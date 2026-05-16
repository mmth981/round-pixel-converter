# Round Pixel HTML Converter

A small Python script that converts an image into a lightweight standalone HTML file rendered as circular dots / round pixels.

The generated HTML does not embed the full-resolution original image. It stores only a reduced color grid, so the output stays smaller.

## Features

- Converts JPG/PNG images into round-pixel HTML artwork
- Uses Python and Pillow
- Creates a self-contained HTML file
- Adjustable dot size, spacing, brightness, contrast, and sampling width
- Good for poster-like dot mosaic experiments

## Requirements

- Python 3.9+
- Pillow

## Installation

```bash
python -m pip install pillow
```

## Quick Start

1. Put an image in this folder (example: `photo.jpg`).
2. Run:

```bash
python round_pixel_html.py photo.jpg output.html
```

3. Open `output.html` in your browser.

You will see an interactive round-pixel version of your image with sliders for:

- **Dot size**
- **Spacing**

## CLI Usage

```bash
python round_pixel_html.py INPUT_IMAGE OUTPUT_HTML [options]
```

### Positional arguments

- `INPUT_IMAGE` — path to your source image
- `OUTPUT_HTML` — path for generated HTML file

### Options

- `--width INT` (default `90`)
  - Sampling width in dots.
  - Lower values = smaller HTML output and more abstract look.
  - Higher values = more detail and larger output.
- `--dot INT` (default `6`)
  - Initial dot size shown in the HTML viewer.
- `--spacing INT` (default `1`)
  - Initial spacing between dots.
- `--brightness FLOAT` (default `1.0`)
  - Brightness multiplier applied before sampling.
- `--contrast FLOAT` (default `1.08`)
  - Contrast multiplier applied before sampling.
- `--check-deps`
  - Checks whether Pillow is installed and exits (useful for environment setup/CI checks).

## Example Commands

Basic conversion:

```bash
python round_pixel_html.py portrait.png portrait_round.html
```

More detailed sampling:

```bash
python round_pixel_html.py portrait.png portrait_round.html --width 140
```

Bolder visual style:

```bash
python round_pixel_html.py portrait.png portrait_round.html --brightness 1.05 --contrast 1.2
```

Different starting dot style:

```bash
python round_pixel_html.py portrait.png portrait_round.html --dot 8 --spacing 2
```

## How to Tune Output

- If output file is too large: lower `--width`
- If image looks too flat: increase `--contrast` slightly (e.g. `1.15`)
- If image looks too dark: raise `--brightness` slightly (e.g. `1.05`)
- If circles blend together too much: increase `--spacing`

## Troubleshooting

- **`ModuleNotFoundError: No module named 'PIL'`**
  - Install Pillow with `python -m pip install pillow`
  - You can also run `python round_pixel_html.py --check-deps` to verify dependency status quickly
- **Output looks stretched or squashed**
  - Use the original image orientation and avoid extreme browser zoom
- **`python` command not found**
  - Try `python3` instead

## License

MIT (see `LICENSE`)
