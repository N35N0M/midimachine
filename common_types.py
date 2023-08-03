from __future__ import print_function

import dataclasses
import enum
from colour import Color


@dataclasses.dataclass
class RgbPixel:
    red: int  # 0-255
    green: int  # 0-255
    blue: int  # 0-255

def from_color_to_rgb_pixel(color: Color) -> RgbPixel:
    return RgbPixel(
        red=int(color.red*255),
        green=int(color.green*255),
        blue=int(color.blue*255)
    )



class UpdateFrequency(enum.Enum):
    BEAT = 1
    HALF_BEAT = 2
    QUARTER_BEAT = 3
    EVERY_OTHER_BEAT = 4