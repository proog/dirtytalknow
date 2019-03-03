import io
import logging
import os
import os.path
import textwrap
from . import ASSETS_PATH
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_FILE = os.path.join(ASSETS_PATH, "fonts/joystix.ttf")
IMAGE_DIR = os.path.join(ASSETS_PATH, "images")


def make_image_with_text(filename: str, text: str):
    img = Image.open(filename)
    img = img.filter(ImageFilter.BLUR)
    draw = ImageDraw.Draw(img)

    (font, wrapped_text) = fit_text_to_image(FONT_FILE, text, img.width, img.height)
    draw.multiline_text((7, 2), wrapped_text, font=font, fill=(0, 0, 0))
    draw.multiline_text((5, 0), wrapped_text, font=font, fill=(170, 25, 150))

    output = io.BytesIO()
    img.save(output, format="jpeg", quality=100)
    return output


def write_image_to_file(image: io.BytesIO, filename: str):
    image.seek(0)
    with open(filename, "wb") as f:
        f.write(image.read())


def get_available_images():
    _, _, filenames = next(os.walk(IMAGE_DIR))
    return [os.path.join(IMAGE_DIR, filename) for filename in filenames]


def fit_text_to_image(font_name: str, text: str, img_width: int, img_height: int):
    img = Image.new("1", (img_width, img_height))
    draw = ImageDraw.Draw(img)
    padding = 5
    max_width = img_width - padding
    max_height = img_height - padding
    attempts = 0

    # decrease line width, then font size, until a fit is achieved
    for font_size in range(100, 12, -1):
        font = ImageFont.truetype(font_name, font_size)

        for line_width in range(30, 10, -1):
            attempts += 1
            wrapped_text = textwrap.fill(text, width=line_width)
            (text_width, text_height) = draw.multiline_textsize(wrapped_text, font=font)

            if text_width <= max_width and text_height <= max_height:
                logging.info("Fit text to image in %i attempts", attempts)
                return (font, wrapped_text)

    raise Exception("Couldn't fit text to image: %s" % text)
