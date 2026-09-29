import json
import subprocess
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont

# nanoemoji's default `--build_dir`, relative to the working directory.
BUILD_DIR = Path("build")
COLOR_FORMATS = [
    "glyf",
    "glyf_colr_0",
    "glyf_colr_1",
    "cff_colr_0",
    "cff_colr_1",
    "cff2_colr_0",
    "cff2_colr_1",
    "picosvg",
    "picosvgz",
    "untouchedsvg",
    "untouchedsvgz",
    "cbdt",
    "sbix",
]


def _make_config(
    *, output_name: str, family: str, color_format: str, paths: list[str]
) -> str:
    return f"""
output_file = {json.dumps(output_name)}
color_format = "{color_format}"
family = {json.dumps(family)}
# Half of nanoemoji's 1024-unit defaults: 512 units are plenty for emoji and
# keep more outline deltas within a single byte, shrinking glyf noticeably.
upem = 512
width = 638
ascender = 475
descender = -125

[axis.wght]
name = "Weight"
default = 400

[master.regular]
style_name = "Regular"
srcs = {json.dumps(paths, indent=2)}

[master.regular.position]
wght = 400
"""


def build_font(*, output: str, family: str, color_format: str, paths: list[str]):
    """Builds `build/<output>` with nanoemoji.

    An output ending in `.woff2` is built as an sfnt first and then compressed.
    """
    woff2 = output.lower().endswith(".woff2")
    if woff2 and color_format.startswith("cff"):
        # nanoemoji picks the sfnt flavor from the output extension.
        sfnt_name = str(Path(output).with_suffix(".otf"))
    elif woff2:
        sfnt_name = str(Path(output).with_suffix(".ttf"))
    else:
        sfnt_name = output

    config = _make_config(
        output_name=sfnt_name,
        family=family,
        color_format=color_format,
        paths=paths,
    )
    with tempfile.NamedTemporaryFile("w", suffix=".toml", delete_on_close=False) as f:
        f.write(config)
        f.close()

        subprocess.run(["nanoemoji", f.name], check=True)

    if woff2:
        font = TTFont(BUILD_DIR / sfnt_name)
        font.flavor = "woff2"
        font.save(BUILD_DIR / output)
