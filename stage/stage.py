from __future__ import print_function

import dataclasses

from dragon.dragon import Dragon
from lightbar.lightbar import LightBar


@dataclasses.dataclass
class Stage_2023:
    """
    Represents the stage for the 2023 show.
    """
    lightbar_one: LightBar
    lightbar_two: LightBar
    lightbar_three: LightBar
    dragon_left: Dragon
    dragon_right: Dragon


def create_stage() -> Stage_2023:
    # Create some lightbars and dragons
    lightbar_one = LightBar(label="Left lightbar")
    lightbar_two = LightBar(label="Middle lightbar")
    lightbar_three = LightBar(label="Right lightbar")

    dragon_one = Dragon(label="Left dragon")
    dragon_two = Dragon(label="Right dragon")

    return Stage_2023(
        lightbar_one=lightbar_one,
        lightbar_two=lightbar_two,
        lightbar_three=lightbar_three,
        dragon_left=dragon_one,
        dragon_right=dragon_two
    )