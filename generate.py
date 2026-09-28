import os
from pathlib import Path
import argparse
import shutil
from build_font import COLOR_FORMATS, build_font
from fill_emojis import fill_emojis

SELF_DIR = Path(__file__).parent


def copy_emojis() -> Path:
    dir = SELF_DIR / "build" / "twemoji"
    dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(SELF_DIR / "twemoji" / "assets" / "svg", dir, dirs_exist_ok=True)
    return dir


def main():
    parser = argparse.ArgumentParser(
        "generate.py", description="Generate a twemoji font"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file name (e.g. font.ttf or font.woff2)",
        required=True,
    )
    parser.add_argument("--family", help="The name of the font family", required=True)
    parser.add_argument(
        "color_format",
        help="The format of the glyphs",
        choices=COLOR_FORMATS,
    )
    args = parser.parse_args()

    dist_dir = copy_emojis()
    fill_emojis(dist_dir)

    build_font(
        output=args.output,
        family=args.family,
        color_format=args.color_format,
        paths=[str(dist_dir / it) for it in os.listdir(dist_dir)],
    )


if __name__ == "__main__":
    main()
