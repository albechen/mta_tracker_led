# %%
import time
from datetime import datetime
import os
import traceback

from rgbmatrix import RGBMatrix, RGBMatrixOptions

from mta_arrival_fetcher import get_all_arrivals
from led_image_renderer import render_image
from led_image_pre_render import create_pre_render

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
LAST_GOOD = ([("error", "-")] * NUM_TRAINS,)

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
    options.hardware_mapping = "adafruit-hat-pwm"

    # performance / flicker settings
    options.brightness = 20  # 0–100
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
    last_pre_render_date = None

    try:
        while True:
            # Check if we need to update the pre-render (new day)
            today_date = datetime.now().strftime("%Y%m%d")

            if today_date != last_pre_render_date:
                pre_render_path = (
                    f"assets/led_matrix_render/pre_render_{today_date}.png"
                )

                # If pre-render doesn't exist, create it
                if not os.path.exists(pre_render_path):
                    print(f"No pre-render found for {today_date}, creating...")

                    create_pre_render()

                    last_pre_render_date = today_date

            try:
                manhattan, queens = get_all_arrivals(FEEDS, LINES, STOP, NUM_TRAINS)
                last_good = (manhattan, queens)
                print(last_good, flush=True)

            except Exception:
                print("⚠️  MTA fetch error:")
                traceback.print_exc()
                manhattan, queens = LAST_GOOD  # last_good

            # Only redraw if data changed OR pre-render changed
            current = (tuple(manhattan), tuple(queens))
            if current != last_displayed:
                image = render_image(manhattan, queens, pre_render_path)
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
