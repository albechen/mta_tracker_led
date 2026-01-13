# %%
import requests
from datetime import datetime


def convert_temp_c_to_f(c):
    return int(c * 9 / 5) + 32


def get_min_max_temp_from_grid(lat, lon):

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


def get_min_max_temp_from_forecast(lat, lon):

    # static
    headers = {"User-Agent": "MyWeatherApp/1.0 (youremail@example.com)"}
    today = str(datetime.now().date())

    # get closest point
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    points_response = requests.get(points_url, headers=headers)
    points_data = points_response.json()

    # get grid date
    forecast_url = points_data["properties"]["forecast"]
    forecast_response = requests.get(forecast_url, headers=headers)
    forecast_data = forecast_response.json()

    # check if C
    should_convert = False
    temperatureUnit = forecast_data["properties"]["periods"][0]["temperatureUnit"]
    if temperatureUnit == "F":
        should_convert = False

    # extract min max temp
    max_temp = -999
    min_temp = 999

    for x in forecast_data["properties"]["periods"]:
        if x["startTime"][:10] == today:

            temp = x["temperature"]

            if should_convert == True:
                temp = convert_temp_c_to_f(temp)

            if temp > max_temp:
                max_temp = temp
            if temp < min_temp:
                min_temp = temp

    return {"high": max_temp, "low": min_temp, "unit": "F"}


# %%
# lat, lon = 40.757546, -73.919102
# get_min_max_temp_from_forecast(lat, lon)

# %%
# # get_min_max_temp(lat, lon)
# headers = {"User-Agent": "MyWeatherApp/1.0 (youremail@example.com)"}
# today = str(datetime.now().date())

# # get closest point
# points_url = f"https://api.weather.gov/points/{lat},{lon}"
# points_response = requests.get(points_url, headers=headers)
# points_data = points_response.json()
# # %%
# points_data

# #%%
# grid_url = points_data["properties"]["forecastGridData"]
# grid_response = requests.get(grid_url, headers=headers)
# grid_data = grid_response.json()

# grid_data

# #%%
# today = "2026-01-13"

# for x in grid_data["properties"]["maxTemperature"]["values"]:
#     if x["validTime"][:10] == today:
#         max_temp = convert_temp_c_to_f(x["value"])
#         break

# for x in grid_data["properties"]["minTemperature"]["values"]:
#     if x["validTime"][:10] == today:
#         min_temp = convert_temp_c_to_f(x["value"])
#         break

# print(max_temp, min_temp)


# #%%

# forecast_url = points_data["properties"]["forecast"]
# forecast_response = requests.get(forecast_url, headers=headers)
# forecast_data = forecast_response.json()

# #%%
# for x in forecast_data["properties"]['periods']:
#     date = x["startTime"][1:10]
#     if date == "today":
#         x['temperature']
#     print(x["startTime"][1:10], x['temperature'])
# %%
