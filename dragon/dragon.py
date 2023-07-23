from __future__ import print_function

from common_types import RgbPixel
from utils import generate_random_color


class Dragon:
    def __init__(self, label: str):
        self.left_eye: RgbPixel = generate_random_color()
        self.right_eye: RgbPixel = generate_random_color()
        self.smoke_machine_on: bool = False # Smoke machines should always prefer OFF. Expensive...
        self.label = label