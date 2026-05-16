# Round Pixel HTML Converter

A small Python script that converts an image into a lightweight standalone HTML file rendered as circular dots / round pixels.

The generated HTML does not embed the full-resolution original image. It stores only a reduced color grid, so the output stays smaller.

## Features

- Converts JPG/PNG images into round-pixel HTML artwork
- Uses Python and Pillow
- Creates a self-contained HTML file
- Adjustable dot size, spacing, brightness, contrast, and sampling width
- Good for poster-like dot mosaic experiments

## Installation

```bash
pip install pillow
