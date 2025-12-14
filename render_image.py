#%%
from PIL import Image, ImageDraw, ImageFont
import time

# -------------------------------------------------
# Canvas
# -------------------------------------------------
WIDTH, HEIGHT = 128, 32

# -------------------------------------------------
# Fonts
# -------------------------------------------------
FONT_SMALL = ImageFont.load("fonts/pil/5x7.pil")
FONT_LARGE = ImageFont.load("fonts/pil/7x14B.pil")

FONT_SMALL_H = 6
FONT_SMALL_W = 4

FONT_LARGE_H = 10
FONT_LARGE_W = 6

MINS_TXT_H = 6
MINS_TXT_W = 14

# https://www.cl.cam.ac.uk/~mgk25/ucs-fonts.html


# -------------------------------------------------
# Icons
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

def draw_icon(image, x, y, line, size, large=False):
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
# def text_size(draw, text, font):
#     box = draw.textbbox((0, 0), text, font=font)
#     return box[2] - box[0], box[3] - box[1]

def text_size(txt, font):
    img = Image.new("1", (180, 20), 0)  # temp large enough
    draw = ImageDraw.Draw(img)
    draw.text((0,0), txt, font=font, fill=1)

    # Crop to actual content
    bbox = img.getbbox()  # bounding box of nonzero pixels
    cropped = img.crop(bbox)
    w, h = cropped.size
    return w, h

def draw_train_large(image, draw, x, col_two_x_offset, y, line, mins):

    middle_y = (32-y)/2 + y
    bullet_y = int((middle_y - BULLET_LARGE_SIZE/2)//1)

    draw_icon(image, x, bullet_y, line, BULLET_LARGE_SIZE, large=True)

    gap_btw_text_num = 2
    min_num_w, min_num_h = text_size(str(mins), FONT_LARGE)
    min_total_h = gap_btw_text_num + min_num_h + MINS_TXT_H

    min_num_y = int((middle_y - min_total_h/2)//1) - 2
    min_txt_y = int((middle_y - min_total_h/2 + gap_btw_text_num + min_num_h)//1)
    
    num_x_start = x + BULLET_LARGE_SIZE + 1
    num_x_end = x + (col_two_x_offset - 1)
    middle_x = (num_x_end - num_x_start) / 2 + num_x_start

    min_num_x = int((middle_x - (min_num_w / 2))//1)
    min_txt_x = int((middle_x - (MINS_TXT_W / 2))//1)

    draw.text((min_num_x, min_num_y), str(mins), (255, 255, 255), FONT_LARGE)

    draw.text(
        (min_txt_x, min_txt_y),
        "min",
        minute_color(mins),
        FONT_SMALL
    )

def draw_train_small(image, draw, x, y, line, mins):

    draw_icon(image, x, y, line, BULLET_SMALL_SIZE)

    num_x = x + BULLET_SMALL_SIZE + 2
    num_y = y + 2

    draw.text((num_x, num_y), str(mins), (255, 255, 255), FONT_SMALL)
    num_w, _ = text_size(str(mins), FONT_SMALL)

    draw.text(
        (num_x + num_w +1, num_y),
        "m",
        minute_color(mins),
        FONT_SMALL
    )



# -------------------------------------------------
# Draw ONE 64x32 side
# -------------------------------------------------
def draw_side(image, draw, x_offset, label, trains):
    draw.text((x_offset, 0), label, (255, 255, 0), FONT_SMALL)

    height_small_font = 7
    col_two_x_offset = 38

    draw_train_large(image, draw, x_offset, col_two_x_offset, height_small_font, *trains[0])

    y_positions = [8, 20]
    for i in range(1, 3):
        draw_train_small(
            image,
            draw,
            x_offset + col_two_x_offset,
            y_positions[i - 1],
            *trains[i]
        )

# -------------------------------------------------
# Image renderer
# -------------------------------------------------
def render_image(manhattan, queens):
    image = Image.new("RGB", (128, 32), (55, 55, 55))
    draw = ImageDraw.Draw(image)

    draw_side(image, draw, 0,  "Manhattan", manhattan)
    draw_side(image, draw, 64, "Queens",  queens)

    # matrix.SetImage(image)

    image.save("test.png")


    # --- Create grid-separated image ---
    orig_width, orig_height = image.size
    zoom = 2  # each pixel becomes 2x2 with 1 black pixel in between
    grid_width = orig_width + (orig_width - 1)
    grid_height = orig_height + (orig_height - 1)

    grid_image = Image.new("RGB", (grid_width, grid_height), (0, 0, 0))
    orig_pixels = image.load()
    grid_pixels = grid_image.load()

    for y in range(orig_height):
        for x in range(orig_width):
            # Position in grid image
            gx = x * 2
            gy = y * 2
            grid_pixels[gx, gy] = orig_pixels[x, y]  # original pixel
            # the extra pixel at gx+1, gy+1, etc. remain black

    grid_image.save("test_grid.png")
    
# -------------------------------------------------
# Arrival fetch (replace with real MTA logic)
# -------------------------------------------------
def get_latest_arrivals():
    # Example placeholder data
    manhattan = [("E", 5), ("R", 7), ("M", 9)]
    queens    = [("R", 19), ("E", 31), ("F", 48)]

    # Regenerate image every time this runs
    render_image(manhattan, queens)

get_latest_arrivals()
# -------------------------------------------------
# Main loop
# -------------------------------------------------

# from rgbmatrix import RGBMatrix, RGBMatrixOptions

# def init_matrix():
#     options = RGBMatrixOptions()
#     options.rows = 32
#     options.cols = 64
#     options.chain_length = 2
#     options.parallel = 1
#     options.hardware_mapping = 'adafruit-hat'

#     matrix = RGBMatrix(options=options)
#     return matrix

# if __name__ == "__main__":
#     matrix = init_matrix()

#     while True:
#         manhattan, queens = get_latest_arrivals()
#         render_image(manhattan, queens, matrix)
#         time.sleep(30)
# %%
