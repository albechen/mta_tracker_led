# %%
import requests
from datetime import datetime

LAT = 40.7644
LON = -73.9235


def apply_gamma(brightness, gamma=2.2, max_brightness=100):
    normalized = brightness / max_brightness
    corrected = normalized**gamma
    return int(corrected * max_brightness)


def get_twilight_epochs(date_str):
    """
    Returns a dict of UTC epoch seconds for twilight times.
    """
    url = "https://api.sunrise-sunset.org/json"
    params = {"lat": LAT, "lng": LON, "date": date_str, "formatted": 0}

    r = requests.get(url, timeout=5, params=params)
    r.raise_for_status()

    results = r.json()["results"]

    def to_epoch(key):
        return int(datetime.fromisoformat(results[key]).timestamp())

    return {
        "nautical_begin": to_epoch("nautical_twilight_begin"),
        "civil_begin": to_epoch("civil_twilight_begin"),
        "civil_end": to_epoch("civil_twilight_end"),
        "nautical_end": to_epoch("nautical_twilight_end"),
    }


def compute_brightness(
    now_epoch, twilight, night_brightness=55, day_brightness=70, gamma=2.2
):
    nb = twilight["nautical_begin"]
    cb = twilight["civil_begin"]
    ce = twilight["civil_end"]
    ne = twilight["nautical_end"]

    # Night before nautical twilight
    if now_epoch < nb:
        brightness = night_brightness

    # Fade-in: nautical → civil
    elif nb <= now_epoch <= cb:
        progress = (now_epoch - nb) / (cb - nb)
        brightness = night_brightness + progress * (day_brightness - night_brightness)

    # Daytime
    elif cb < now_epoch < ce:
        brightness = day_brightness

    # Fade-out: civil → nautical
    elif ce <= now_epoch <= ne:
        progress = (now_epoch - ce) / (ne - ce)
        brightness = day_brightness - progress * (day_brightness - night_brightness)

    # Night after nautical twilight
    else:
        brightness = night_brightness

    brightness = apply_gamma(brightness, gamma)

    return brightness


# %%
# =================================================
# Test runner
# =================================================
# from datetime import datetime, timezone, timedelta
# from zoneinfo import ZoneInfo


# today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# twilight = get_twilight_epochs(today)

# print("\nTwilight test for", today)
# print("-" * 50)

# print(
#     "Nautical begin:",
#     datetime.fromtimestamp(twilight["nautical_begin"], tz=timezone.utc)
#     .astimezone(ZoneInfo("America/New_York"))
#     .strftime("%I:%M %p"),
# )
# print(
#     "Civil begin   :",
#     datetime.fromtimestamp(twilight["civil_begin"], tz=timezone.utc)
#     .astimezone(ZoneInfo("America/New_York"))
#     .strftime("%I:%M %p"),
# )
# print(
#     "Civil end     :",
#     datetime.fromtimestamp(twilight["civil_end"], tz=timezone.utc)
#     .astimezone(ZoneInfo("America/New_York"))
#     .strftime("%I:%M %p"),
# )
# print(
#     "Nautical end  :",
#     datetime.fromtimestamp(twilight["nautical_end"], tz=timezone.utc)
#     .astimezone(ZoneInfo("America/New_York"))
#     .strftime("%I:%M %p"),
# )

# print("-" * 50)

# # Start at midnight UTC
# start = datetime.now(timezone.utc).replace(
#     hour=0, minute=0, second=0, microsecond=0
# )
# end = start + timedelta(days=1)

# t = start
# while t < end:
#     epoch = int(t.timestamp())

#     brightness = compute_brightness(epoch, twilight)
#     gamma_brighness = compute_gamma_brightness(brightness)

#     label = ""
#     if twilight["nautical_begin"] <= epoch <= twilight["civil_begin"]:
#         label = "↗ fade-in (naut → civil)"
#     elif twilight["civil_end"] <= epoch <= twilight["nautical_end"]:
#         label = "↘ fade-out (civil → naut)"
#     elif twilight["civil_begin"] < epoch < twilight["civil_end"]:
#         label = "☀ day"
#     else:
#         label = "🌙 night"

#     ny_time = t.astimezone(ZoneInfo("America/New_York")).strftime("%I:%M:%S %p")
#     print(f"{ny_time} | brightness {gamma_brighness} {brightness:.2f} {label}")

#     t += timedelta(seconds=20)


# %%
# url = "https://api.sunrise-sunset.org/json"
# params = {"lat": LAT, "lng": LON, "date": "2026-01-13", "formatted": 0}  # YYYY-MM-DD

# r = requests.get(url, timeout=5, params=params)
# r.raise_for_status()
# data = r.json()["results"]

# sunrise_epoch = int(datetime.fromisoformat(data["sunrise"]).timestamp())
# sunset_epoch = int(datetime.fromisoformat(data["sunset"]).timestamp())


# %%
# test gamma output
# def apply_gamma(brightness, gamma=2.2, max_brightness=100):
#     normalized = brightness / max_brightness
#     corrected = normalized ** gamma
#     return int(corrected * max_brightness)

# for x in range(100):
#     print(x, apply_gamma(x))
# 0 0
# 1 0
# 2 0
# 3 0
# 4 0
# 5 0
# 6 0
# 7 0
# 8 0
# 9 0
# 10 0
# 11 0
# 12 0
# 13 1
# 14 1
# 15 1
# 16 1
# 17 2
# 18 2
# 19 2
# 20 2
# 21 3
# 22 3
# 23 3
# 24 4
# 25 4
# 26 5
# 27 5
# 28 6
# 29 6
# 30 7
# 31 7
# 32 8
# 33 8
# 34 9
# 35 9
# 36 10
# 37 11
# 38 11
# 39 12
# 40 13
# 41 14
# 42 14
# 43 15
# 44 16
# 45 17
# 46 18
# 47 18
# 48 19
# 49 20
# 50 21
# 51 22
# 52 23
# 53 24
# 54 25
# 55 26
# 56 27
# 57 29
# 58 30
# 59 31
# 60 32
# 61 33
# 62 34
# 63 36
# 64 37
# 65 38
# 66 40
# 67 41
# 68 42
# 69 44
# 70 45
# 71 47
# 72 48
# 73 50
# 74 51
# 75 53
# 76 54
# 77 56
# 78 57
# 79 59
# 80 61
# 81 62
# 82 64
# 83 66
# 84 68
# 85 69
# 86 71
# 87 73
# 88 75
# 89 77
# 90 79
# 91 81
# 92 83
# 93 85
# 94 87
# 95 89
# 96 91
# 97 93
# 98 95
# 99 97
