from __future__ import print_function

from common_types import RgbPixel
from utils import generate_random_color


class Dragon:
    def __init__(self, label: str):
        self.left_eye: RgbPixel = generate_random_color()
        """NOTE that this does not do RGB color blend, it is just R, G nad B"""
        self.right_eye: RgbPixel = generate_random_color()
        """NOTE that this does not do RGB color blend, it is just R, G nad B"""
        self.smoke_machine_on: bool = False # Smoke machines should always prefer OFF. Expensive...
        self.label = label