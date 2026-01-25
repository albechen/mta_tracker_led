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
