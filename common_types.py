from __future__ import print_function

import dataclasses
import enum


@dataclasses.dataclass
class RgbPixel:
    red: int  # 0-255
    green: int  # 0-255
    blue: int  # 0-255


class UpdateFrequency(enum.Enum):
    BEAT = 1
    HALF_BEAT = 2
    QUARTER_BEAT = 3
    EVERY_OTHER_BEAT = 4