from __future__ import print_function

import typing

from common_types import RgbPixel
from utils import generate_random_color


class LightBar:
    """
    A class for working with the lightbar in 96 channel mode.
    TODO: Light bar model name name

    """

    def __init__(self, label: str):
        self.pixels: typing.List[RgbPixel] = [generate_random_color() for _ in range(32)]
        self.label = label

    def set_pixel(self, pixel: int, color: RgbPixel):
        if pixel > 31:
            raise ValueError("Pixel value must be less than 32.")
        self.pixels[pixel] = color

    def clear_pixels(self):
        for i in range(len(self.pixels)):
            self.pixels[i] = RgbPixel(0, 0, 0)