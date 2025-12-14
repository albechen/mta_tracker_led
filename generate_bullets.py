#%%
from PIL import Image, ImageDraw, ImageFont
import os

# -------------------------------------------------
# Config
# -------------------------------------------------
LINES = ["R", "E", "M", "F"]
BULLET_LARGE_SIZE = 16
BULLET_SMALL_SIZE = 8

ICON_DIR_LARGE = "icons/large_bullet"
ICON_DIR_SMALL = "icons/small_bullet"

os.makedirs(ICON_DIR_LARGE, exist_ok=True)
os.makedirs(ICON_DIR_SMALL, exist_ok=True)

LINE_BG_COLORS = {
    "R": (252, 204, 10),
    "E": (0, 57, 166),
    "M": (255, 99, 25),
    "F": (255, 99, 25),
}

LINE_TXT_COLORS = {
    "R": (0, 0, 0),
    "E": (255, 255, 255),
    "M": (255, 255, 255),
    "F": (255, 255, 255),
}

FONT_SMALL_BULLET = ImageFont.load("fonts/pil/5x8.pil")
FONT_LARGE_BULLET = ImageFont.load("fonts/pil/7x14B.pil")

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def text_size(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]

def generate_icon(size, line, font, out_path):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    r = size // 2
    draw.ellipse(
        (0, 0, size - 1, size - 1),
        fill=LINE_BG_COLORS[line]
    )

    tw, th = text_size(draw, line, font)
    draw.text(
        (r - tw // 2, r - th // 2),
        line,
        fill=LINE_TXT_COLORS[line],
        font=font
    )

    img.save(out_path)

# -------------------------------------------------
# Generate icons
# -------------------------------------------------
for line in LINES:
    generate_icon(
        BULLET_SMALL_SIZE,
        line,
        FONT_SMALL_BULLET,
        f"{ICON_DIR_SMALL}/{line}_{BULLET_SMALL_SIZE}.png"
    )
    generate_icon(
        BULLET_LARGE_SIZE,
        line,
        FONT_LARGE_BULLET,
        f"{ICON_DIR_LARGE}/{line}_{BULLET_LARGE_SIZE}.png"
    )

print("Icons generated.")

# %%
