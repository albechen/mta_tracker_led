# %%
from PIL import Image, ImageDraw, ImageFont

# Load font
FONT_SMALL = ImageFont.load("assets/fonts/pil/5x7.pil")

# Test values
high = 27
low = 14

high_text = str(high)
low_text = str(low)


# Helpers
def text_w(font, text):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]


def text_h(font, text="8"):
    bbox = font.getbbox(text)
    return bbox[3] - bbox[1]


# Layout
gap = 1
line_h = text_h(FONT_SMALL)

# Colors
BG = (20, 20, 20)
RED = (255, 60, 60)
BLUE = (60, 140, 255)
GRAY = (200, 200, 200)

# Measure total width
high_w = text_w(FONT_SMALL, high_text)
low_w = text_w(FONT_SMALL, low_text)

total_width = high_w + gap + 1 + gap + 1 + gap + low_w + gap + 1  # dot  # line  # dot

# Image
WIDTH = total_width + 20
HEIGHT = line_h + 20

img = Image.new("RGB", (WIDTH, HEIGHT), BG)
draw = ImageDraw.Draw(img)

# Position
x = 10
baseline_y = 10

# ---- Draw High ----
draw.text((x, baseline_y), high_text, RED, FONT_SMALL)
x += high_w + gap - 1  # pull back 1px to cancel font padding

# ---- Draw Dot ----
dot_y = baseline_y + 1
draw.point((x, dot_y), fill=RED)
x += 1 + gap

# ---- Draw Line ----
draw.line((x, baseline_y, x, baseline_y + line_h - 1), fill=GRAY, width=1)
x += 1 + gap

# ---- Draw Low ----
draw.text((x, baseline_y), low_text, BLUE, FONT_SMALL)
x += low_w + gap - 1  # same fix here

# ---- Draw Dot ----
dot_y = baseline_y + 1
draw.point((x, dot_y), fill=BLUE)


# Save
img.save("weather_test.png")
print("Saved as weather_test.png")


# %%
import requests
from datetime import datetime, timezone
from math import fabs


def get_led_brightness(
    day_brightness: int,
    night_brightness: int,
    shortwave_radiation: float,
    cloudcover: float,
    max_radiation: float = 900.0,
) -> int:
    # Night detection
    if shortwave_radiation <= 1:
        return night_brightness

    sun_factor = min(shortwave_radiation / max_radiation, 1.0)
    cloud_factor = 1.0 - min(max(cloudcover, 0), 100) / 100.0

    light_factor = sun_factor * cloud_factor
    brightness_range = day_brightness - night_brightness

    brightness = night_brightness + (brightness_range * light_factor)
    return int(round(brightness))


def get_current_weather_data(latitude: float, longitude: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "shortwave_radiation,cloudcover",
        "timezone": "America/New_York",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_closest_hour_index(times, current_time):
    closest_index = 0
    smallest_diff = float("inf")

    for i, t in enumerate(times):
        api_time = datetime.fromisoformat(t)
        diff = fabs((api_time - current_time).total_seconds())
        if diff < smallest_diff:
            smallest_diff = diff
            closest_index = i

    return closest_index


def get_brightness_from_open_meteo(
    latitude: float, longitude: float, day_brightness: int, night_brightness: int
) -> int:
    data = get_current_weather_data(latitude, longitude)

    hourly = data["hourly"]
    times = hourly["time"]

    # Current local time (matches API timezone=auto)
    now = datetime.now().replace(tzinfo=None)

    idx = get_closest_hour_index(times, now)

    radiation = hourly["shortwave_radiation"][idx]
    cloudcover = hourly["cloudcover"][idx]

    return get_led_brightness(day_brightness, night_brightness, radiation, cloudcover)


LAT = 40.7128  # New York
LON = -74.0060

brightness = get_brightness_from_open_meteo(
    latitude=LAT, longitude=LON, day_brightness=255, night_brightness=10
)

print("LED Brightness:", brightness)

# %%
LAT = 40.7128  # New York
LON = -74.0060
data = get_current_weather_data(LAT, LON)
hourly = data["hourly"]
hourly

# %%
times = hourly["time"]
radiation = hourly["shortwave_radiation"]
cloudcover = hourly["cloudcover"]


# %%

from datetime import datetime


def print_weather_table_ampm(hourly):
    times = hourly["time"]
    radiation = hourly["shortwave_radiation"]
    cloudcover = hourly["cloudcover"]

    # Table header
    header = f"{'Local Date':<12} {'Local Time':<12} {'Radiation (W/m²)':<18} {'Cloud Cover (%)':<16}"
    print(header)
    print("-" * len(header))

    for t, rad, cloud in zip(times, radiation, cloudcover):
        dt = datetime.fromisoformat(t)

        local_date = dt.date().isoformat()
        local_time = dt.strftime("%I:%M %p")  # 12-hour format with AM/PM

        row = f"{local_date:<12} {local_time:<12} {rad:<18} {cloud:<16}"
        print(row)


# -------------------
# Example Usage
# -------------------
LAT = 40.7128  # New York
LON = -74.0060

data = get_current_weather_data(LAT, LON)
hourly = data["hourly"]

print_weather_table_ampm(hourly)
