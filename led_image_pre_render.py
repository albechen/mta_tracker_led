# %%
# pre_render.py
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Import the rendering functions from the original code
WIDTH, HEIGHT = 128, 32

FONT_SMALL = ImageFont.load("assets/fonts/pil/5x7.pil")
FONT_TINY = ImageFont.load("assets/fonts/pil/4x6.pil")

# Assuming you have a weather function in a separate module
from get_weather_high_low import get_min_max_temp  # Adjust import as needed


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
    draw.text((manhattan_x, label_y), "Manhattan", (255, 255, 0), FONT_SMALL)

    # Draw Queens label
    draw.text((queens_x, label_y), "Queens", (255, 255, 0), FONT_SMALL)

    # 2. Get today's high and low temperatures
    try:
        # Get coordinates for Queens area
        # Using approximate coordinates for Queens, NY
        queens_lat, queens_lon = 40.7282, -73.7949

        weather_data = get_min_max_temp(queens_lat, queens_lon)

        if weather_data:
            high = int(weather_data.get("high", "--"))
            low = int(weather_data.get("low", "--"))

            # Create weather text
            weather_text = f"{high}°/{low}°"
            print(f"Weather text: {weather_text}")

            # Calculate text width using the actual font
            # For 4x6 font, each character is approximately 4 pixels wide
            # Let's measure it more accurately
            text_bbox = FONT_TINY.getbbox(weather_text)
            text_width = text_bbox[2] - text_bbox[0]  # right - left

            # Anchor to the very right edge
            # Subtract 1 pixel to account for 0-based indexing (128 width = pixels 0-127)
            weather_x = WIDTH - text_width + 1  # Last pixel touching right edge

            # Alternative: if you want it perfectly flush with right edge
            # weather_x = WIDTH - text_width  # Will leave 1 pixel gap on right

            draw.text((weather_x, label_y), weather_text, (120, 255, 120), FONT_TINY)

            # Optional: Draw a debug pixel at the right edge
            # draw.point((WIDTH-1, label_y+2), fill=(255, 0, 0))

    except Exception as e:
        print(f"Error getting weather: {e}")
        # Draw placeholder if weather fails, also anchored to right
        placeholder_text = "--|--"
        text_bbox = FONT_TINY.getbbox(placeholder_text)
        text_width = text_bbox[2] - text_bbox[0]
        weather_x = WIDTH - text_width - 1
        draw.text((weather_x, label_y), placeholder_text, (255, 130, 0), FONT_TINY)

    # 3. Save to file
    output_dir = "assets/led_matrx_render"
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


if __name__ == "__main__":
    # Run pre-render when executed directly
    create_pre_render()

# %%
