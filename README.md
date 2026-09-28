# twemoji-colr-font

This repository contains [Twemoji](https://github.com/jdecked/twemoji) emojis as an OpenType font using [nanoemoji](https://github.com/googlefonts/nanoemoji). It is a fork of [Nerixyz/twemoji-colr-font](https://github.com/Nerixyz/twemoji-colr-font) that targets Chromium (WebView2 and CEF) only.

**The latest builds can be found [here](https://github.com/ZeWaka/twemoji-colr-font/releases)**.

Each release contains:

- `Twemoji_GlyfColr1.woff2`: [glyf] [COLR]v1, WOFF2-compressed, for use via `@font-face`
- `Twemoji_GlyfColr1.ttf`: the same font uncompressed, e.g. for `gen-segoeui.py`

[COLR]: https://learn.microsoft.com/en-us/typography/opentype/spec/colr
[glyf]: https://learn.microsoft.com/en-us/typography/opentype/spec/glyf

You can generate the font locally too (requires [uv](https://docs.astral.sh/uv)):

```sh
git submodule update --init --recursive
uv run generate.py glyf_colr_1 -o font.woff2 --family "Twemoji - COLRv1"
```

The font will be located in the `build/` directory. An output name ending in `.woff2` builds the `.ttf` first and then compresses it to WOFF2 next to it.

On Windows, you can use `gen-segoeui.py` to set the name of a font to `Segoe UI Emoji` (copies the name from the default font). This font can then be installed and will get added as a replacement for the default Windows emoji font.

```sh
uv run gen-segoeui.py build/Twemoji_GlyfColr1.ttf -o build/SegoeUI_Twemoji.ttf
```
