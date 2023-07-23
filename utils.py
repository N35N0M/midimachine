from __future__ import print_function

import random

from common_types import RgbPixel


def generate_random_color() -> RgbPixel:
    return RgbPixel(
        red=random.randint(0, 255),
        green=random.randint(0, 255),
        blue=random.randint(0, 255)
    )