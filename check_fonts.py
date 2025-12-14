#%%
from PIL import ImageFont

FONT_SMALL = ImageFont.load("fonts/pil/7x14B.pil")

# Characters to check
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

for c in chars:
    mask = FONT_SMALL.getmask(c)
    width, height = mask.size
    print(f"Character: {c} => Width: {width}, Height: {height}")

#%%
from PIL import Image, ImageDraw, ImageFont

# Load bitmap fonts
FONT_SMALLEST = ImageFont.load("fonts/pil/4x6.pil")
FONT_SMALL = ImageFont.load("fonts/pil/5x7.pil")
FONT_LARGE = ImageFont.load("fonts/pil/7x14B.pil")

def print_glyph_pixels(font):
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        # Create an image just big enough
        img = Image.new("1", (20, 20), 0)  # temp large enough
        draw = ImageDraw.Draw(img)
        draw.text((0,0), c, font=font, fill=1)

        # Crop to actual content
        bbox = img.getbbox()  # bounding box of nonzero pixels
        if bbox:
            cropped = img.crop(bbox)
            w, h = cropped.size
            print(f"{c}: {w}x{h} pixels")
            # Print pixels
            for y in range(h):
                line = "".join(["#" if cropped.getpixel((x,y)) else "." for x in range(w)])
                print(line)
        print()

print("SMALLEST FONT")
print_glyph_pixels(FONT_SMALLEST)

print("SMALL FONT")
print_glyph_pixels(FONT_SMALL)

print("LARGE FONT")
print_glyph_pixels(FONT_LARGE)


#%%
def text_size(txt, font):
    img = Image.new("1", (180, 20), 0)  # temp large enough
    draw = ImageDraw.Draw(img)
    draw.text((0,0), txt, font=font, fill=1)

    # Crop to actual content
    bbox = img.getbbox()  # bounding box of nonzero pixels
    if bbox:
        cropped = img.crop(bbox)
        w, h = cropped.size
        print(f"{txt}: {w}x{h} pixels")
        # Print pixels
        for y in range(h):
            line = "".join(["#" if cropped.getpixel((x,y)) else "." for x in range(w)])
            print(line)

text_size("21", FONT_LARGE)