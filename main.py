# %%
import time
import traceback

from rgbmatrix import RGBMatrix, RGBMatrixOptions

from mta_arrival_fetcher import get_all_arrivals
from led_image_renderer import render_image

# =================================================
# Configuration
# =================================================
LINES = ["R", "E", "F", "M"]
STOP = "G19"
NUM_TRAINS = 3

FEEDS = [
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",
]

REFRESH_SECONDS = 20

# Placeholder used if nothing has ever loaded
LAST_GOOD = (
    [("E", 99)] * NUM_TRAINS,
    [("E", 99)] * NUM_TRAINS,
)

# manhattan, queens = get_all_arrivals(FEEDS, LINES, STOP, NUM_TRAINS)
# image = render_image(manhattan, queens)

# -------------------------------------------------
# Main loop
# -------------------------------------------------


def init_matrix():
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 2
    options.parallel = 1
    options.hardware_mapping = "adafruit-hat"

    # ⭐ Important performance / flicker settings
    options.brightness = 50  # 0–100
    options.pwm_bits = 11  # lower = faster
    options.pwm_lsb_nanoseconds = 130
    options.limit_refresh_rate_hz = 200

    return RGBMatrix(options=options)


# =================================================
# Main loop
# =================================================
def main():
    matrix = init_matrix()

    last_good = LAST_GOOD
    last_displayed = None  # used to avoid unnecessary redraws

    try:
        while True:
            try:
                manhattan, queens = get_all_arrivals(FEEDS, LINES, STOP, NUM_TRAINS)
                last_good = (manhattan, queens)

            except Exception:
                print("⚠️  MTA fetch error:")
                traceback.print_exc()
                manhattan, queens = last_good

            # Only redraw if data changed
            current = (tuple(manhattan), tuple(queens))
            if current != last_displayed:
                image = render_image(manhattan, queens)
                matrix.SetImage(image)
                last_displayed = current

            time.sleep(REFRESH_SECONDS)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down cleanly...")
        matrix.Clear()


# =================================================
# Entry point
# =================================================
if __name__ == "__main__":
    main()

# %%
