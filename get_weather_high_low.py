# %%
import requests
from datetime import datetime


def convert_temp_c_to_f(c):
    return int(c * 9 / 5) + 32


def get_min_max_temp(lat, lon):

    # static
    headers = {"User-Agent": "MyWeatherApp/1.0 (youremail@example.com)"}
    today = str(datetime.now().date())

    # get closest point
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    points_response = requests.get(points_url, headers=headers)
    points_data = points_response.json()

    # get grid date
    grid_url = points_data["properties"]["forecastGridData"]
    grid_response = requests.get(grid_url, headers=headers)
    grid_data = grid_response.json()

    # check if C
    should_convert = False
    wmoUnit = grid_data["properties"]["maxTemperature"]["uom"]
    if wmoUnit == "wmoUnit:degC":
        should_convert = True

    # extract min max temp
    for x in grid_data["properties"]["maxTemperature"]["values"]:
        if x["validTime"][:10] == today:
            if should_convert == True:
                max_temp = convert_temp_c_to_f(x["value"])
            else:
                max_temp = x["value"]
            break

    for x in grid_data["properties"]["minTemperature"]["values"]:
        if x["validTime"][:10] == today:
            if should_convert == True:
                min_temp = convert_temp_c_to_f(x["value"])
            else:
                min_temp = x["value"]
            break

    return {"high": max_temp, "low": min_temp, "unit": "F"}


# lat, lon = 40.7128, -74.0060
# get_min_max_temp(lat, lon)

# %%
