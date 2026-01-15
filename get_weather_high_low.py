# %%
import requests
from datetime import datetime


def convert_temp_c_to_f(c):
    return int(c * 9 / 5) + 32


def get_min_max_temp_weathergov(LAT, LON):

    # static
    headers = {"User-Agent": "MyWeatherApp/1.0 (youremail@example.com)"}
    today = str(datetime.now().date())

    # get closest point
    points_url = f"https://api.weather.gov/points/{LAT},{LON}"
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

    return {"high": max_temp, "low": min_temp}


def get_min_max_temp_openmetro(lat, lon):
    today = str(datetime.now().date())

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": "fahrenheit",
        "timezone": "America/New_York",
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()

    dates = data["daily"]["time"]
    max_temps = data["daily"]["temperature_2m_max"]
    min_temps = data["daily"]["temperature_2m_min"]

    for i, date in enumerate(dates):
        if date == today:
            return {"high": round(max_temps[i]), "low": round(min_temps[i])}

    raise ValueError("Today's forecast not found")


# LAT = 40.7644
# LON = -73.9235
# print(get_min_max_temp_weathergov(LAT, LON))
# print(get_min_max_temp_openmetro(LAT, LON))
# %%
