# %%
# pre_render.py
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Import the rendering functions from the original code
WIDTH, HEIGHT = 128, 32

FONT_SMALL = ImageFont.load("assets/fonts/pil/5x7.pil")
FONT_TINY = ImageFont.load("assets/fonts/pil/4x6.pil")

LAT = 40.7644
LON = -73.9235

from get_weather_high_low import get_min_max_temp_openmetro


def create_pre_render():
    """
    Create pre-rendered image with Manhattan/Queens labels and today's weather
    Save as pre_render_{today_date}.png and clean up old files
    """
    # Get today's date
    today_date = datetime.now().strftime("%Y%m%d")

    # Create base image
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # 1. Pre-render Manhattan and Queens labels
    manhattan_x = 0
    queens_x = WIDTH // 2
    label_y = 0

    # Draw Manhattan label (yellow)
    draw.text((manhattan_x, label_y), "Manhattan", (255, 255, 255), FONT_SMALL)

    # Draw Queens label
    draw.text((queens_x, label_y), "Queens", (255, 255, 255), FONT_SMALL)

    # 2. Get today's high and low temperatures
    try:
        # Get coordinates for Queens area
        # Using approximate coordinates for Queens, NY

        weather_data = get_min_max_temp_openmetro(LAT, LON)

        if weather_data:
            high = int(weather_data.get("high", "--"))
            low = int(weather_data.get("low", "--"))

            high_text = f"{high}°"
            sep_text = "|"
            low_text = f"{low}°"

            # Measure widths
            high_w = FONT_SMALL.getbbox(high_text)[2]
            sep_w = FONT_SMALL.getbbox(sep_text)[2] - 1
            low_w = FONT_SMALL.getbbox(low_text)[2]

            total_width = high_w + sep_w + low_w

            # Right-align the whole group
            weather_x = WIDTH - total_width

            x = weather_x + 1

            # Draw high (bright red)
            draw.text((x, label_y), high_text, (255, 60, 60), FONT_SMALL)
            x += high_w

            # Draw separator
            draw.text((x, label_y), sep_text, (200, 200, 200), FONT_SMALL)
            x += sep_w

            # Draw low (bright blue)
            draw.text((x, label_y), low_text, (60, 140, 255), FONT_SMALL)

    except Exception as e:
        print(f"Error getting weather: {e}")
        # Draw placeholder if weather fails, also anchored to right
        placeholder_text = "--|--"
        text_bbox = FONT_SMALL.getbbox(placeholder_text)
        text_width = text_bbox[2] - text_bbox[0]
        weather_x = WIDTH - text_width - 1
        draw.text((weather_x, label_y), placeholder_text, (255, 130, 0), FONT_SMALL)

    # 3. Save to file
    output_dir = "assets/led_matrix_render"
    os.makedirs(output_dir, exist_ok=True)

    # Delete old pre-render files
    for filename in os.listdir(output_dir):
        if filename.startswith("pre_render_") and filename.endswith(".png"):
            # Extract date from filename
            file_date = filename.replace("pre_render_", "").replace(".png", "")
            if file_date != today_date:
                try:
                    os.remove(os.path.join(output_dir, filename))
                    print(f"Deleted old pre-render: {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")

    # Save new pre-render
    output_path = os.path.join(output_dir, f"pre_render_{today_date}.png")
    image.save(output_path)
    print(f"Pre-render saved: {output_path}")

    return output_path


create_pre_render()

# %%
