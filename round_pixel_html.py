# round_pixel_html.py
# Convert an image into a small standalone HTML round-pixel mosaic.
#
# Install requirement:
#   pip install pillow
#
# Usage:
#   python round_pixel_html.py input.jpg output.html
#
# Optional:
#   python round_pixel_html.py input.jpg output.html --width 90 --dot 6

from PIL import Image, ImageEnhance
import argparse
import json
import os


def image_to_color_grid(
    image_path,
    sample_width=90,
    brightness=1.0,
    contrast=1.08,
):
    """
    Opens an image, resizes it to a small sampling grid,
    and returns width, height, and RGB color values.
    """

    img = Image.open(image_path).convert("RGB")

    # Preserve aspect ratio
    original_width, original_height = img.size
    aspect_ratio = original_height / original_width
    sample_height = max(1, int(sample_width * aspect_ratio))

    # Slightly improve visual punch for dot rendering
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)

    # Downsample heavily
    small = img.resize((sample_width, sample_height), Image.Resampling.LANCZOS)

    colors = []
    for y in range(sample_height):
        row = []
        for x in range(sample_width):
            r, g, b = small.getpixel((x, y))
            row.append([r, g, b])
        colors.append(row)

    return sample_width, sample_height, colors


def make_html(width, height, colors, dot_size=6, spacing=1, title="Round Pixel Render"):
    """
    Creates a standalone HTML file with canvas rendering.
    """

    color_data = json.dumps(colors, separators=(",", ":"))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
  body {{
    margin: 0;
    min-height: 100vh;
    background: #111;
    color: #eee;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    padding: 24px;
    box-sizing: border-box;
  }}

  h1 {{
    font-size: 18px;
    font-weight: 500;
    margin: 0;
    opacity: 0.85;
  }}

  .controls {{
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    font-size: 14px;
  }}

  label {{
    display: flex;
    gap: 8px;
    align-items: center;
  }}

  input[type="range"] {{
    width: 150px;
  }}

  .stage {{
    max-width: 95vw;
    max-height: 82vh;
    overflow: auto;
    background: #080808;
    padding: 16px;
    border-radius: 18px;
    box-shadow: 0 16px 48px rgba(0,0,0,0.45);
  }}

  canvas {{
    display: block;
    max-width: 100%;
    height: auto;
  }}
</style>
</head>

<body>

<h1>{title}</h1>

<div class="controls">
  <label>
    Dot size
    <input id="dotSize" type="range" min="2" max="18" value="{dot_size}">
    <span id="dotValue">{dot_size}</span>
  </label>

  <label>
    Spacing
    <input id="spacing" type="range" min="0" max="8" value="{spacing}">
    <span id="spacingValue">{spacing}</span>
  </label>
</div>

<div class="stage">
  <canvas id="canvas"></canvas>
</div>

<script>
const gridWidth = {width};
const gridHeight = {height};
const colors = {color_data};

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const dotSlider = document.getElementById("dotSize");
const spacingSlider = document.getElementById("spacing");
const dotValue = document.getElementById("dotValue");
const spacingValue = document.getElementById("spacingValue");

function draw() {{
  const dot = Number(dotSlider.value);
  const spacing = Number(spacingSlider.value);
  const cell = dot + spacing;

  dotValue.textContent = dot;
  spacingValue.textContent = spacing;

  canvas.width = gridWidth * cell;
  canvas.height = gridHeight * cell;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let y = 0; y < gridHeight; y++) {{
    for (let x = 0; x < gridWidth; x++) {{
      const [r, g, b] = colors[y][x];

      ctx.fillStyle = `rgb(${{r}}, ${{g}}, ${{b}})`;

      const cx = x * cell + cell / 2;
      const cy = y * cell + cell / 2;
      const radius = dot / 2;

      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, Math.PI * 2);
      ctx.fill();
    }}
  }}
}}

dotSlider.addEventListener("input", draw);
spacingSlider.addEventListener("input", draw);

draw();
</script>

</body>
</html>
"""

    return html


def convert_image_to_round_pixel_html(
    input_path,
    output_path,
    sample_width=90,
    dot_size=6,
    spacing=1,
    brightness=1.0,
    contrast=1.08,
):
    width, height, colors = image_to_color_grid(
        input_path,
        sample_width=sample_width,
        brightness=brightness,
        contrast=contrast,
    )

    title = os.path.splitext(os.path.basename(input_path))[0] + " - Round Pixel Render"

    html = make_html(
        width=width,
        height=height,
        colors=colors,
        dot_size=dot_size,
        spacing=spacing,
        title=title,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Done: {output_path}")
    print(f"Sample grid: {width} x {height}")
    print(f"Output size: {os.path.getsize(output_path) / 1024:.1f} KB")


def main():
    parser = argparse.ArgumentParser(
        description="Convert an image into a small standalone HTML round-pixel mosaic."
    )

    parser.add_argument("input", help="Input image path, e.g. photo.jpg")
    parser.add_argument("output", help="Output HTML path, e.g. output.html")

    parser.add_argument(
        "--width",
        type=int,
        default=90,
        help="Sampling width in dots. Smaller = smaller file. Default: 90",
    )

    parser.add_argument(
        "--dot",
        type=int,
        default=6,
        help="Default dot size in pixels. Default: 6",
    )

    parser.add_argument(
        "--spacing",
        type=int,
        default=1,
        help="Default spacing between dots. Default: 1",
    )

    parser.add_argument(
        "--brightness",
        type=float,
        default=1.0,
        help="Brightness multiplier. Default: 1.0",
    )

    parser.add_argument(
        "--contrast",
        type=float,
        default=1.08,
        help="Contrast multiplier. Default: 1.08",
    )

    args = parser.parse_args()

    convert_image_to_round_pixel_html(
        input_path=args.input,
        output_path=args.output,
        sample_width=args.width,
        dot_size=args.dot,
        spacing=args.spacing,
        brightness=args.brightness,
        contrast=args.contrast,
    )


if __name__ == "__main__":
    main()
