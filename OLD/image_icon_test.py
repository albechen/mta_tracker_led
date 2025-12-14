#%%
from PIL import Image, ImageDraw, ImageFont

# -------------------------------------------------
# Canvas
# -------------------------------------------------
WIDTH, HEIGHT = 128, 32
image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(image)

# -------------------------------------------------
# Fonts
# -------------------------------------------------
FONT_SMALL = ImageFont.load("fonts/pil/5x7.pil")
FONT_LARGE = ImageFont.load("fonts/pil/7x14B.pil")

# -------------------------------------------------
# Load icons
# -------------------------------------------------
ICON_CACHE = {}

BULLET_LARGE_SIZE = 16
BULLET_SMALL_SIZE = 10

def load_icon(line, size, large=False):
    key = (line, size, large)
    if key not in ICON_CACHE:
        folder = "icons/large_bullet" if large else "icons/small_bullet"
        path = f"{folder}/{line}_{size}.png"
        ICON_CACHE[key] = Image.open(path).convert("RGBA")
    return ICON_CACHE[key]

def draw_icon(x, y, line, size, large=False):
    icon = load_icon(line, size, large)
    image.paste(icon, (x, y), icon)

# -------------------------------------------------
# Minute color logic
# -------------------------------------------------
def minute_color(mins):
    if mins < 6:
        return (255, 120, 120)
    elif mins < 8:
        return (255, 170, 90)
    elif mins < 10:
        return (255, 230, 120)
    else:
        return (160, 255, 160)

# -------------------------------------------------
# Drawing helpers
# -------------------------------------------------
def text_size(text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]

def draw_train_small(x, y, line, mins):
    draw_icon(x, y, line, BULLET_SMALL_SIZE, large=False)

    num_x = x + BULLET_SMALL_SIZE + 2
    num_y = y + 2

    draw.text((num_x, num_y), str(mins), fill=(255, 255, 255), font=FONT_SMALL)
    num_w, _ = text_size(str(mins), FONT_SMALL)

    draw.text(
        (num_x + num_w + 1, num_y),
        "m",
        fill=minute_color(mins),
        font=FONT_SMALL
    )

def draw_train_large(x, col_two_x_offset, y, line, mins):
    draw_icon(x, y, line, BULLET_LARGE_SIZE, large=True)

    num_w, _ = text_size(str(mins), FONT_LARGE)
    num_x_start = x + BULLET_LARGE_SIZE + 1
    num_x_end = x + (col_two_x_offset - 1)
    num_x = (num_x_end - num_x_start) / 2 + num_x_start - (num_w / 2)
    num_y = y - 2

    draw.text((num_x, num_y), str(mins), fill=(255, 255, 255), font=FONT_LARGE)

    mins_w, _ = text_size("min", FONT_SMALL)
    mins_x = (num_x_end - num_x_start) / 2 + num_x_start - (mins_w / 2)

    draw.text(
        (mins_x, num_y + 14),
        "min",
        fill=minute_color(mins),
        font=FONT_SMALL
    )

# -------------------------------------------------
# Draw ONE 64x32 side
# -------------------------------------------------
def draw_side(x_offset, label, trains):
    draw.text((x_offset, 0), label, fill=(255, 255, 0), font=FONT_SMALL)

    col_two_x_offset = 36

    draw_train_large(x_offset, col_two_x_offset, 11, *trains[0])

    y_positions = [0, 11, 22]
    for i in range(1, 4):
        draw_train_small(
            x_offset + col_two_x_offset,
            y_positions[i - 1],
            *trains[i]
        )

# -------------------------------------------------
# Example data
# -------------------------------------------------
manhattan = [("E", 12), ("R", 4), ("M", 24), ("F", 99)]
queens = [("R", 25), ("E", 31), ("F", 48), ("M", 99)]

draw_side(0, "Manhttn", manhattan)
draw_side(64, "Queens", queens)

image.show()
image.save("test.png")
