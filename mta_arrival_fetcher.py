# %%
import requests
from datetime import datetime
from google.transit import gtfs_realtime_pb2


def process_feed(feed, lines, stop_prefix, now):
    queens = []
    manhattan = []

    for entity in feed.entity:
        trip = entity.trip_update
        if not trip:
            continue

        route = trip.trip.route_id
        if route not in lines:
            continue

        for stu in trip.stop_time_update:
            if not stu.stop_id.startswith(stop_prefix):
                continue
            if not stu.arrival or stu.arrival.time <= 0:
                continue

            diff_secs = stu.arrival.time - now
            diff_mins = diff_secs // 60

            if diff_mins < 5 or diff_mins >= 45:
                continue

            entry = (route, diff_mins)
            direction = stu.stop_id[-1]

            if direction == "N":
                queens.append(entry)
            elif direction == "S":
                manhattan.append(entry)

    return queens, manhattan


def get_all_arrivals(feed_urls, lines, stop, num_arrivals=3):
    now = int(datetime.now().timestamp())
    queens_all = []
    manhattan_all = []

    session = requests.Session()
    session.headers.update({"User-Agent": "LED-Matrix-Train-Board/1.0"})

    for url in feed_urls:
        feed = gtfs_realtime_pb2.FeedMessage()
        r = session.get(url, timeout=5)
        feed.ParseFromString(r.content)

        q, m = process_feed(feed, lines, stop, now)
        queens_all.extend(q)
        manhattan_all.extend(m)

    queens_all.sort(key=lambda x: x[1])
    manhattan_all.sort(key=lambda x: x[1])

    return (
        manhattan_all[:num_arrivals],
        queens_all[:num_arrivals],
    )


# %%
####################
#### EXAMPLE #####
####################

# lines_of_interest = ["R", "E", "F", "M"]
# stop_of_interest = "G19"
# num_arrivals = 3

# feed_list = [
#     "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
#     "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
#     "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",
# ]

# manhattan_arrivals, queens_arrivals = get_all_arrivals(
#     feed_list, lines_of_interest, stop_of_interest, num_arrivals
# )

# print("Queens next arrivals:")
# for r in queens_arrivals:
#     print(r)

# print("\nManhattan next arrivals:")
# for r in manhattan_arrivals:
#     print(r)

# %%
