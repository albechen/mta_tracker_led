#%%
from PIL import Image, ImageDraw, ImageFont


#%%
# -------------------------------------------------
# Canvas (matches LED resolution)
# -------------------------------------------------
WIDTH, HEIGHT = 128, 32
image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(image)

# -------------------------------------------------
# Fonts
# -------------------------------------------------
import os
# https://www.cl.cam.ac.uk/~mgk25/ucs-fonts.html
# FONT_SMALL = ImageFont.load_default()
# FONT_SMALL_BULLET = ImageFont.load_default()
FONT_SMALL = ImageFont.load("fonts/pil/5x7.pil")
FONT_SMALL_BULLET = ImageFont.load("fonts/pil/5x8.pil")
FONT_LARGE = ImageFont.load("fonts/pil/7x14B.pil")
FONT_LARGE_BULLET = ImageFont.load("fonts/pil/7x14B.pil")

#
# -------------------------------------------------
# Load icons
# -------------------------------------------------

LINE_BG_COLORS = {
    "R": (252, 204, 10),   # yellow
    "E": (0, 57, 166),     # blue
    "M": (255, 99, 25),    # orange
    "F": (255, 99, 25),    # orange
}

LINE_TXT_COLORS = {
    "R": (0, 0, 0),         # white
    "E": (255, 255, 255),   # white
    "M": (255, 255, 255),   # white
    "F": (255, 255, 255),   # white
}

def text_size(text, font_style):
    box = draw.textbbox((0, 0), text, font=font_style)
    return box[2] - box[0], box[3] - box[1]

def draw_icon(x, y, size, line, font_style):
    r = size // 2
    draw.ellipse(
        (x, y, x + size - 1, y + size - 1),
        fill=LINE_BG_COLORS[line]
    )
    tw, th = text_size(line, font_style)
    draw.text(
        (x + r - tw // 2, y + r - th // 2),
        line,
        fill=LINE_TXT_COLORS[line],
        font=font_style
    )


# -------------------------------------------------
# Minute suffix color logic
# -------------------------------------------------
def minute_color(mins):
    if mins < 6:
        return (255, 120, 120)   # pale red
    elif mins < 8:
        return (255, 170, 90)    # pale orange
    elif mins < 10:
        return (255, 230, 120)   # pale yellow
    else:
        return (160, 255, 160)   # pale green

# -------------------------------------------------
# Drawing helpers
# -------------------------------------------------
def draw_train_small(x, y, size, line, mins):

    draw_icon(x, y, size, line, FONT_SMALL_BULLET)

    num_x = x + size + 2
    num_y = y + 2

    # Number (white)
    draw.text(
        (num_x, num_y),
        str(mins),
        fill=(255, 255, 255),
        font=FONT_SMALL
    )

    num_w, _ = text_size(str(mins), FONT_SMALL)

    # Colored "m"
    draw.text(
        (num_x + num_w + 1, num_y),
        "m",
        fill=minute_color(mins),
        font=FONT_SMALL
    )

def draw_train_large(x, col_two_x_offset, y, size, line, mins):

    draw_icon(x, y, size, line, FONT_LARGE_BULLET)

    num_w, _ = text_size(str(mins), FONT_LARGE)
    num_x_start = x + size + 1
    num_x_end = x + (col_two_x_offset-1)
    num_x = (num_x_end - num_x_start) / 2 + num_x_start - (num_w / 2)

    # print(num_x_start, num_x_end, num_x)

    num_y = y - 2

    # Number (white)
    draw.text(
        (num_x, num_y),
        str(mins),
        fill=(255, 255, 255),
        font=FONT_LARGE,
        align="middle"
    )

    mins_w, _ = text_size(str("min"), FONT_SMALL)
    mins_x = (num_x_end - num_x_start) / 2 + num_x_start - (mins_w / 2)

    draw.text(
        (mins_x, num_y + 14),
        "min",
        fill=minute_color(mins),
        font=FONT_SMALL,
        align="middle"
    )

# -------------------------------------------------
# Draw ONE 64x32 side
# -------------------------------------------------
def draw_side(x_offset, label, trains):
    # Direction label
    draw.text(
        (x_offset, 0),
        label,
        fill=(255, 255, 0),
        font=FONT_SMALL
    )

    col_two_x_offset = 36

    # Big train (21x21)
    draw_train_large(x_offset, col_two_x_offset, 11, 16, *trains[0])

    # Small trains (10x10)
    y_positions = [0, 11, 22]
    for i in range(1, 4):
        draw_train_small(
            x_offset + col_two_x_offset,
            y_positions[i - 1],
            10,
            *trains[i]
        )

# -------------------------------------------------
# Example data (replace later with MTA API)
# -------------------------------------------------
manhattan = [("E", 12), ("R", 4), ("M", 24), ("F", 99)]
queens    = [("R", 25), ("E", 31), ("F", 48), ("M", 99)]

draw_side(0,  "Manhttn", manhattan)
draw_side(64, "Queens", queens)

# -------------------------------------------------
# Show / save image
# -------------------------------------------------
image.show()               # opens default image viewer
# image.save("preview.png")  # optional: save to disk

# %%
