# %%
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =================================================
# Canvas
# =================================================
WIDTH, HEIGHT = 128, 32
BG_COLOR = (0, 0, 0)

# =================================================
# Fonts
# =================================================
FONT_SMALL = ImageFont.load("assets/fonts/pil/5x7.pil")
FONT_LARGE = ImageFont.load("assets/fonts/pil/7x14B.pil")

FONT_SMALL_H = 6
FONT_SMALL_W = 4

FONT_LARGE_H = 10
FONT_LARGE_W = 6

MINS_TXT_H = 6
MINS_TXT_W = 14

# =================================================
# Layout constants
# =================================================
LABEL_Y = 0
LARGE_ROW_Y = 7
SMALL_ROW_Y = (8, 20)

LEFT_COL_WIDTH = 38

# =================================================
# Icons
# =================================================
ICON_CACHE = {}
BULLET_LARGE_SIZE = 16
BULLET_SMALL_SIZE = 10


def load_icon(line, size, large=False):
    """
    Load and cache line bullet icons.
    """
    key = (line, size, large)
    if key not in ICON_CACHE:
        folder = "assets/icons/large_bullet" if large else "assets/icons/small_bullet"
        path = f"{folder}/{line}_{size}.png"
        ICON_CACHE[key] = Image.open(path).convert("RGBA")
    return ICON_CACHE[key]


def draw_icon(image, x, y, line, size, large=False):
    icon = load_icon(line, size, large)
    image.paste(icon, (x, y), icon)


# =================================================
# Minute color logic
# =================================================
def minute_color(mins):
    if mins == "-":
        return (255, 0, 0)
    if mins <= 7:
        return (255, 0, 0)  # red
    if mins <= 9:
        return (255, 130, 0)  # orange
    return (120, 255, 120)  # green


# =================================================
# Train drawing
# =================================================
def draw_train_large(image, draw, x, col_two_x, y, line, mins):
    """
    Draws the primary (large) train entry.
    """
    middle_y = y + (HEIGHT - y) // 2
    bullet_y = middle_y - BULLET_LARGE_SIZE // 2

    draw_icon(image, x, bullet_y, line, BULLET_LARGE_SIZE, large=True)

    mins_str = str(mins)
    mins_num_w = (FONT_LARGE_W + 1) * len(mins_str) - 1

    total_h = FONT_LARGE_H + 1 + MINS_TXT_H
    mins_num_y = middle_y - total_h // 2 - 3
    mins_txt_y = mins_num_y + FONT_LARGE_H + 3

    num_x_start = x + BULLET_LARGE_SIZE + 1
    num_x_end = x + col_two_x - 1
    center_x = num_x_start + (num_x_end - num_x_start) // 2

    mins_num_x = center_x - mins_num_w // 2
    mins_txt_x = center_x - MINS_TXT_W // 2

    draw.text((mins_num_x, mins_num_y), mins_str, (255, 255, 255), FONT_LARGE)
    draw.text(
        (mins_txt_x, mins_txt_y),
        "min",
        minute_color(mins),
        FONT_SMALL,
    )


def draw_train_small(image, draw, x, y, line, mins):
    """
    Draws a secondary (small) train entry.
    """
    draw_icon(image, x, y, line, BULLET_SMALL_SIZE)

    num_x = x + BULLET_SMALL_SIZE + 2
    num_y = y + 2

    mins_str = str(mins)
    draw.text((num_x, num_y), mins_str, (255, 255, 255), FONT_SMALL)

    mins_w = (FONT_SMALL_W + 1) * len(mins_str) - 1
    draw.text(
        (num_x + mins_w + 1, num_y),
        "m",
        minute_color(mins),
        FONT_SMALL,
    )


# =================================================
# Side renderer (64x32)
# =================================================

PLACEHOLDER = ("error", "-")


def draw_side(image, draw, x_offset, label, trains):
    """
    Draws one half (Manhattan / Queens).
    """
    # Ensure exactly 3 entries
    trains = (trains + [PLACEHOLDER] * 3)[:3]

    draw_train_large(
        image,
        draw,
        x_offset,
        LEFT_COL_WIDTH,
        LARGE_ROW_Y,
        *trains[0],
    )

    for i in range(1, 3):
        draw_train_small(
            image,
            draw,
            x_offset + LEFT_COL_WIDTH,
            SMALL_ROW_Y[i - 1],
            *trains[i],
        )

    # --- Draw HH:MM in upper right if Manhattan ---
    if label == "Manhattan":
        now = datetime.now()
        time_str = now.strftime("%I:%M").lstrip("0")  # remove leading zero
        text_w, text_h = draw.textsize(time_str, font=FONT_SMALL)
        # Draw at top right corner of this side
        draw.text(
            (x_offset + LEFT_COL_WIDTH - text_w, LABEL_Y),
            time_str,
            (255, 255, 0),
            FONT_SMALL,
        )


# =================================================
# Image renderer
# =================================================
def render_image(manhattan, queens, pre_render_path):
    """
    Renders the full 128x32 LED matrix image.
    Uses a pre-render if provided, otherwise creates a new base image.
    """
    try:
        # Use the provided pre-render image path
        image = Image.open(pre_render_path).convert("RGB")
    except:
        # Fallback: create a new base image
        image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), "Manhattan", (255, 255, 0), FONT_SMALL)
        draw.text((WIDTH // 2, 0), "Queens", (255, 255, 0), FONT_SMALL)
        print(f"FAILED pre-render for today")

    # Create drawing context
    draw = ImageDraw.Draw(image)
    draw_side(image, draw, 0, "Manhattan", manhattan)
    draw_side(image, draw, WIDTH // 2, "Queens", queens)

    return image


# -------------------------------------------------
# TEST PIXEL LAYOUT USING STATIC DATA
# -------------------------------------------------


def draw_pixel_grid_image(image):
    orig_width, orig_height = image.size
    zoom = 2  # each pixel becomes 2x2 with 1 black pixel in between
    grid_width = orig_width + (orig_width - 1)
    grid_height = orig_height + (orig_height - 1)

    grid_image = Image.new("RGB", (grid_width, grid_height), (55, 55, 55))
    orig_pixels = image.load()
    grid_pixels = grid_image.load()

    for y in range(orig_height):
        for x in range(orig_width):
            # Position in grid image
            gx = x * 2
            gy = y * 2
            grid_pixels[gx, gy] = orig_pixels[x, y]  # original pixel
            # the extra pixel at gx+1, gy+1, etc. remain black

    output_path = "assets/led_matrix_render/"
    image.save(output_path + f"test.png")
    grid_image.save(output_path + f"test_grid.png")


# def get_latest_arrivals():
#     manhattan = [("E", 5), ("R", 9), ("M", 11)]
#     # manhattan = []
#     queens = [("R", 19), ("E", 10), ("F", 49)]

#     image = render_image(manhattan, queens)
#     draw_pixel_grid_image(image)


# get_latest_arrivals()
# %%
