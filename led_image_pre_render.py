# %%
# pre_render.py (refactored)
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 128, 32

FONT_SMALL = ImageFont.load("assets/fonts/pil/5x7.pil")
FONT_TINY = ImageFont.load("assets/fonts/pil/4x6.pil")

LAT = 40.7644
LON = -73.9235

from get_weather_high_low import get_min_max_temp_openmetro

# ----------------------------
# Text / Pixel Helpers
# ----------------------------


def text_w(font, text):
    """Tight width of rendered text (no bearings)."""
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]


def text_h(font, text="8"):
    """Pixel height of font using a tall glyph."""
    bbox = font.getbbox(text)
    return bbox[3] - bbox[1]


# ----------------------------
# Drawing Helpers
# ----------------------------


def draw_labels(draw, y=0):
    """Draw Manhattan and Queens labels."""
    manhattan_x = 0
    queens_x = WIDTH // 2

    draw.text((manhattan_x, y), "Manhtn", (255, 255, 255), FONT_SMALL)
    draw.text((queens_x, y), "Queens", (255, 255, 255), FONT_SMALL)


def draw_weather_row(draw, high, low, y=0):
    """
    Draw right-aligned weather row:
        {high}·|{low}·

    - Dot = single pixel
    - Line = 1px vertical
    - 1px gap between all elements
    - Cancels font right-bearing for pixel-tight spacing
    """

    high_text = str(high)
    low_text = str(low)

    gap = 1
    line_h = text_h(FONT_SMALL)

    # Measure widths
    high_w = text_w(FONT_SMALL, high_text)
    low_w = text_w(FONT_SMALL, low_text)

    total_width = (
        high_w + gap + 1 + gap + 1 + gap + low_w + gap + 1  # dot  # line  # dot
    )

    # Right-align group
    x = WIDTH - total_width + 2

    # ---- Draw High ----
    draw.text((x, y), high_text, (255, 60, 60), FONT_SMALL)
    x += high_w + gap - 1  # cancel font right bearing

    # ---- Draw Dot (1px, raised) ----
    dot_y = y + 1
    draw.point((x, dot_y), fill=(255, 60, 60))
    x += 1 + gap

    # ---- Draw Line ----
    draw.line(
        (x, y, x, y + line_h - 1),
        fill=(200, 200, 200),
        width=1,
    )
    x += 1 + gap

    # ---- Draw Low ----
    draw.text((x, y), low_text, (60, 140, 255), FONT_SMALL)
    x += low_w + gap - 1

    # ---- Draw Dot (1px, raised) ----
    draw.point((x, dot_y), fill=(60, 140, 255))


def draw_weather_placeholder(draw, y=0):
    """Draw fallback placeholder if weather fails."""
    placeholder_text = "--|--"
    bbox = FONT_SMALL.getbbox(placeholder_text)
    width = bbox[2] - bbox[0]

    x = WIDTH - width - 1
    draw.text((x, y), placeholder_text, (255, 130, 0), FONT_SMALL)


# ----------------------------
# File Helpers
# ----------------------------


def cleanup_old_renders(output_dir):
    """Delete old pre-rendered images."""
    for filename in os.listdir(output_dir):
        if filename.startswith("pre_render_") and filename.endswith(".png"):
            try:
                os.remove(os.path.join(output_dir, filename))
                print(f"Deleted old pre-render: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")


# ----------------------------
# Main Entry
# ----------------------------


def create_pre_render():
    """
    Create pre-rendered image with Manhattan/Queens labels and today's weather
    Save as pre_render_{today_date}.png and clean up old files
    """

    got_weather = False
    today_date = datetime.now().strftime("%Y%m%d")

    # Create base image
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    label_y = 0

    # 1. Labels
    draw_labels(draw, label_y)

    # 2. Weather
    try:
        weather_data = get_min_max_temp_openmetro(LAT, LON)

        if weather_data:
            high = int(weather_data.get("high", "--"))
            low = int(weather_data.get("low", "--"))

            draw_weather_row(draw, high, low, label_y)
            got_weather = True

    except Exception as e:
        print(f"Error getting weather: {e}")
        draw_weather_placeholder(draw, label_y)

    # 3. Save
    output_dir = "assets/led_matrix_render"
    os.makedirs(output_dir, exist_ok=True)

    cleanup_old_renders(output_dir)

    output_path = os.path.join(output_dir, f"pre_render_{today_date}.png")
    image.save(output_path)
    print(f"Pre-render saved: {output_path}")

    return got_weather


# create_pre_render()
# %%
