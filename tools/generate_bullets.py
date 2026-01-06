# %%
from PIL import Image, ImageDraw
import math


def red_outlined_circle_with_slash(
    diameter: int, outline_ratio: float = 0.08, slash_ratio: float = 0.12
) -> Image.Image:
    """
    Generate a red outlined circle with a red 45-degree slash inside it.

    :param diameter: Diameter of the circle in pixels
    :param outline_ratio: Thickness of circle outline as fraction of diameter
    :param slash_ratio: Thickness of slash as fraction of diameter
    :return: PIL Image (RGBA)
    """
    img = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = diameter // 2
    outline_width = max(1, int(diameter * outline_ratio))
    slash_width = max(1, int(diameter * slash_ratio))

    # --- Mask for circle (to clip the slash) ---
    mask = Image.new("L", (diameter, diameter), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse(
        (
            outline_width // 2,
            outline_width // 2,
            diameter - outline_width // 2 - 1,
            diameter - outline_width // 2 - 1,
        ),
        fill=255,
    )

    # --- Slash layer ---
    slash_layer = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    slash_draw = ImageDraw.Draw(slash_layer)

    r = center * math.sqrt(2)
    x1, y1 = center - r, center - r
    x2, y2 = center + r, center + r

    slash_draw.line((x1, y1, x2, y2), fill=(255, 0, 0, 255), width=slash_width)

    # Apply mask so slash stays inside circle
    img = Image.composite(slash_layer, img, mask)

    draw = ImageDraw.Draw(img)

    # --- Circle outline ---
    draw.ellipse(
        (
            outline_width // 2,
            outline_width // 2,
            diameter - outline_width // 2 - 1,
            diameter - outline_width // 2 - 1,
        ),
        outline=(255, 0, 0, 255),
        width=outline_width,
    )

    return img


red_outlined_circle_with_slash(16).save("error_16.png")
red_outlined_circle_with_slash(10).save("error_10.png")


# %%
from PIL import Image, ImageDraw, ImageFont
import os

# -------------------------------------------------
# Config
# -------------------------------------------------
LINES = ["R", "E", "M", "F"]
BULLET_LARGE_SIZE = 16
BULLET_SMALL_SIZE = 10

ICON_DIR_LARGE = "assets/icons/large_bullet"
ICON_DIR_SMALL = "assets/icons/small_bullet"

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

FONT_SMALL_BULLET = ImageFont.load("assets/fonts/pil/5x8.pil")
FONT_LARGE_BULLET = ImageFont.load("assets/fonts/pil/7x14B.pil")


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
    draw.ellipse((0, 0, size - 1, size - 1), fill=LINE_BG_COLORS[line])

    tw, th = text_size(draw, line, font)
    draw.text((r - tw // 2, r - th // 2), line, fill=LINE_TXT_COLORS[line], font=font)

    img.save(out_path)


# -------------------------------------------------
# Generate icons
# -------------------------------------------------
for line in LINES:
    generate_icon(
        BULLET_SMALL_SIZE,
        line,
        FONT_SMALL_BULLET,
        f"{ICON_DIR_SMALL}/{line}_{BULLET_SMALL_SIZE}.png",
    )
    generate_icon(
        BULLET_LARGE_SIZE,
        line,
        FONT_LARGE_BULLET,
        f"{ICON_DIR_LARGE}/{line}_{BULLET_LARGE_SIZE}.png",
    )

print("Icons generated.")

# %%
