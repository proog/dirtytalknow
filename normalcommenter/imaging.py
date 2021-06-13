import io
import logging
import os
import os.path
import textwrap

from PIL import Image, ImageDraw, ImageFont

from . import ASSETS_PATH

FONT_FILE = os.path.join(ASSETS_PATH, "fonts/joystix.ttf")
IMAGE_DIR = os.path.join(ASSETS_PATH, "images")


class TextFittingException(Exception):
    pass


def make_image_with_text(filename: str, text: str, position="middle"):
    img = Image.open(filename)

    (text_x, text_y, text_w, text_h) = _get_text_bounds(img, position)
    rectangle_bounds = (text_x, text_y, text_x + text_w, text_y + text_h)
    (font, wrapped_text) = fit_text_to_image(FONT_FILE, text, text_w, text_h)

    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle(rectangle_bounds, fill=(0, 0, 0, 160))
    draw.text((text_x + 3, text_y + 3), wrapped_text, font=font, fill=(0, 0, 0))
    draw.text((text_x + 2, text_y + 2), wrapped_text, font=font, fill=(240, 210, 60))

    output = io.BytesIO()
    img.save(output, format="jpeg", quality=100)
    return output


def write_image_to_file(image: io.BytesIO, filename: str):
    image.seek(0)
    with open(filename, "wb") as f:
        f.write(image.read())


def get_available_images():
    _, _, filenames = next(os.walk(IMAGE_DIR))
    return [
        (os.path.join(IMAGE_DIR, filename), filename.split("_")[0])
        for filename in filenames
        if filename.endswith(".jpg")
    ]


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

        for line_width in range(50, 10, -1):
            attempts += 1
            wrapped_text = textwrap.fill(text, width=line_width)
            (text_width, text_height) = draw.multiline_textsize(wrapped_text, font=font)

            if text_width <= max_width and text_height <= max_height:
                logging.info("Fit text to image in %i attempts", attempts)
                return (font, wrapped_text)

    raise TextFittingException("Couldn't fit text to image: %s" % text)


def _get_text_bounds(image: Image, position: str):
    if position == "top":
        return (0, 0, image.width, int(image.height / 2))
    elif position == "bottom":
        return (0, int(image.height / 2), image.width, int(image.height / 2))
    elif position == "left":
        return (0, 0, int(image.width / 2), image.height)
    elif position == "right":
        return (int(image.width / 2), 0, int(image.width / 2), image.height)

    return (0, 0, image.width, image.height)
