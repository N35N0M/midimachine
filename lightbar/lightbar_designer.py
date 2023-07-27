import dataclasses
import enum
import random
import typing

from lightbar.lightbar import LightBar
from common_types import UpdateFrequency, RgbPixel
from midi.midi_input_handler import MidiInputHandler
from traktor_metadata import TraktorMetadata
from utils import generate_random_color

from collections import deque
from itertools import islice



@dataclasses.dataclass
class RandomUpdateAmountOfLightbars:
    amount_of_lightbars: int = 1

@dataclasses.dataclass
class OrganizedUpdateOfLightbars:
    lightbar_pairings: typing.List[typing.List[int]] = dataclasses.field(default_factory=lambda: [[0],[1],[2]])
    groups_must_have_same_color: bool = True


ColorChangeLightBar = typing.Union[RandomUpdateAmountOfLightbars, OrganizedUpdateOfLightbars]
"""
Either specify a random number of bars to change, or specify pairings to change sequentially.
"""
class Direction(enum.Enum):
    RIGHT = 1
    LEFT = 2

@dataclasses.dataclass
class RandomColorChangesLightBar:
    update_frequency: UpdateFrequency = UpdateFrequency.BEAT
    lightbar_color: typing.List[RgbPixel] = dataclasses.field(
        default_factory=lambda: [generate_random_color() for i in range(3)])
    bar_update_type: ColorChangeLightBar = OrganizedUpdateOfLightbars()
    counter = 0

@dataclasses.dataclass
class RetrowaveGridState:
    update_frequency: UpdateFrequency = UpdateFrequency.BEAT
    color: RgbPixel = RgbPixel(255, 0, 255)  # Purple
    pixels: deque[RgbPixel] = deque([RgbPixel(0, 0, 0) for _ in range(96)])

@dataclasses.dataclass
class TankEngineState:
    update_frequency: UpdateFrequency = UpdateFrequency.BEAT
    counter = 0
    """Draw thomas the tank engine."""
    pixels: deque[RgbPixel] = deque([
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(10, 10, 10),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(10, 10, 10),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(10, 10, 10),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(10, 10, 10),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(10, 10, 10),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(10, 10, 10),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(128, 68, 28),
                                        RgbPixel(10, 10, 10),
                                        RgbPixel(25, 25, 255),
                                        RgbPixel(25, 25, 255),
                                        RgbPixel(25, 25, 255),
                                        RgbPixel(107, 107, 107),
                                    ] + [RgbPixel(0, 0, 0) for _ in range(96 - 25)])

class Mode(enum.Enum):
    DRAW_TOWARDS_RIGHT = 1
    RAINBOW_BLINK = 2
    BLINK = 3
    BEAT_SQUARE = 4
    BEAT_SQUARE_BOUNCING = 5
    RANDOM_LIGHTBAR_CHANGES_COLOR = RandomColorChangesLightBar()
    THOMAS_THE_DANK_ENGINE = 7
    RETROWAVE_GRID = 8

class UpdateType(enum.Enum):
    PULSE = 1
    BEAT = 2

class LightbarDesigner:
    def __init__(self, midi_clock, lightbar_left, lightbar_right, lightbar_center, traktor_metadata: TraktorMetadata):
        self.midi_clock: MidiInputHandler = midi_clock
        self.lightbar_left: LightBar = lightbar_left
        self.lightbar_center: LightBar = lightbar_center
        self.lightbar_right: LightBar = lightbar_right
        self.traktor_metadata: TraktorMetadata = traktor_metadata
        self.current_color = generate_random_color()
        self.mode = Mode.RANDOM_LIGHTBAR_CHANGES_COLOR
        self.modestate:  typing.Union[TankEngineState, RetrowaveGridState, None] = None
        self.direction = Direction.RIGHT
        self.pulse_effect_started = False
        self.internal_pulse_counter = 0
        self.internal_beat_counter = 0

        self.midi_clock.notify_on_pulse(self.on_pulse)
        self.midi_clock.notify_on_beat(self.on_beat)

    def set_mode(self, mode):
        self.mode = mode

    def on_pulse(self):
        self.internal_pulse_counter += 1
        self.render(UpdateType.PULSE)

    def on_beat(self):
        self.internal_beat_counter += 1
        self.render(UpdateType.BEAT)

    def render(self, update_type: UpdateType):
        # PREPROGRAMMED SONGS

        # TODO: Only do the following when a master switch takes place!
        if self.traktor_metadata.current_track_deck_a == "Biggie smalls the tank engine":
            self.mode = Mode.THOMAS_THE_DANK_ENGINE
            self.modestate = TankEngineState()
        if self.traktor_metadata.current_track_deck_a == "The Girl and the Robot":
            self.mode = Mode.RETROWAVE_GRID
            if not isinstance(self.modestate, RetrowaveGridState):
                self.modestate = RetrowaveGridState()


            # First, shift all the current pixels outwards.
            if self.internal_pulse_counter % 24 == 0:
                # On every beat, shift every pixel left/right.
                left_side = deque(islice(self.modestate.pixels, 0, 48))
                right_side = deque(islice(self.modestate.pixels, 48, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + right_side

            if self.internal_pulse_counter % 24 == 1:
                left_side = deque(islice(self.modestate.pixels, 0, 46))
                frozen_middle = deque(islice(self.modestate.pixels, 46, 50))
                right_side = deque(islice(self.modestate.pixels, 50, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 2:
                left_side = deque(islice(self.modestate.pixels, 0, 44))
                frozen_middle = deque(islice(self.modestate.pixels, 44, 52))
                right_side = deque(islice(self.modestate.pixels, 52, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 3:
                left_side = deque(islice(self.modestate.pixels, 0, 42))
                frozen_middle = deque(islice(self.modestate.pixels, 42, 54))
                right_side = deque(islice(self.modestate.pixels, 54, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 4:
                left_side = deque(islice(self.modestate.pixels, 0, 40))
                frozen_middle = deque(islice(self.modestate.pixels, 40, 56))
                right_side = deque(islice(self.modestate.pixels, 56, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 5:
                left_side = deque(islice(self.modestate.pixels, 0, 38))
                frozen_middle = deque(islice(self.modestate.pixels, 38, 58))
                right_side = deque(islice(self.modestate.pixels, 58, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 6:
                left_side = deque(islice(self.modestate.pixels, 0, 36))
                frozen_middle = deque(islice(self.modestate.pixels, 36, 60))
                right_side = deque(islice(self.modestate.pixels, 60, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side


            if self.internal_pulse_counter % 24 == 7:
                left_side = deque(islice(self.modestate.pixels, 0, 34))
                frozen_middle = deque(islice(self.modestate.pixels, 34, 62))
                right_side = deque(islice(self.modestate.pixels, 58, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 8:
                left_side = deque(islice(self.modestate.pixels, 0, 32))
                frozen_middle = deque(islice(self.modestate.pixels, 32, 64))
                right_side = deque(islice(self.modestate.pixels, 60, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 9:
                left_side = deque(islice(self.modestate.pixels, 0, 30))
                frozen_middle = deque(islice(self.modestate.pixels, 30, 66))
                right_side = deque(islice(self.modestate.pixels, 62, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 10:
                left_side = deque(islice(self.modestate.pixels, 0, 28))
                frozen_middle = deque(islice(self.modestate.pixels, 28, 68))
                right_side = deque(islice(self.modestate.pixels, 64, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 11:
                left_side = deque(islice(self.modestate.pixels, 0, 26))
                frozen_middle = deque(islice(self.modestate.pixels, 26, 70))
                right_side = deque(islice(self.modestate.pixels, 66, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 12:
                left_side = deque(islice(self.modestate.pixels, 0, 24))
                frozen_middle = deque(islice(self.modestate.pixels, 24, 72))
                right_side = deque(islice(self.modestate.pixels, 68, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 13:
                left_side = deque(islice(self.modestate.pixels, 0, 22))
                frozen_middle = deque(islice(self.modestate.pixels, 22, 74))
                right_side = deque(islice(self.modestate.pixels, 70, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 14:
                left_side = deque(islice(self.modestate.pixels, 0, 20))
                frozen_middle = deque(islice(self.modestate.pixels, 20, 76))
                right_side = deque(islice(self.modestate.pixels, 72, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 15:
                left_side = deque(islice(self.modestate.pixels, 0, 18))
                frozen_middle = deque(islice(self.modestate.pixels, 18, 78))
                right_side = deque(islice(self.modestate.pixels, 74, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 16:
                left_side = deque(islice(self.modestate.pixels, 0, 16))
                frozen_middle = deque(islice(self.modestate.pixels, 16, 80))
                right_side = deque(islice(self.modestate.pixels, 76, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 17:
                left_side = deque(islice(self.modestate.pixels, 0, 14))
                frozen_middle = deque(islice(self.modestate.pixels, 14, 82))
                right_side = deque(islice(self.modestate.pixels, 78, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 18:
                left_side = deque(islice(self.modestate.pixels, 0, 12))
                frozen_middle = deque(islice(self.modestate.pixels, 12, 84))
                right_side = deque(islice(self.modestate.pixels, 80, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 19:
                left_side = deque(islice(self.modestate.pixels, 0, 10))
                frozen_middle = deque(islice(self.modestate.pixels, 10, 86))
                right_side = deque(islice(self.modestate.pixels, 82, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 20:
                left_side = deque(islice(self.modestate.pixels, 0, 8))
                frozen_middle = deque(islice(self.modestate.pixels, 8, 88))
                right_side = deque(islice(self.modestate.pixels, 84, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 21:
                left_side = deque(islice(self.modestate.pixels, 0, 6))
                frozen_middle = deque(islice(self.modestate.pixels, 6, 90))
                right_side = deque(islice(self.modestate.pixels, 86, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 22:
                left_side = deque(islice(self.modestate.pixels, 0, 4))
                frozen_middle = deque(islice(self.modestate.pixels, 4, 92))
                right_side = deque(islice(self.modestate.pixels, 88, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side

            if self.internal_pulse_counter % 24 == 23:
                left_side = deque(islice(self.modestate.pixels, 0, 2))
                frozen_middle = deque(islice(self.modestate.pixels, 2, 94))
                right_side = deque(islice(self.modestate.pixels, 90, 96))
                left_side.rotate(-1)
                right_side.rotate(1)
                self.modestate.pixels = left_side + frozen_middle + right_side



            if self.internal_pulse_counter % 24 == 0:
                # Spawn a new pixel on every beat.
                self.modestate.pixels[47] = self.modestate.color
                self.modestate.pixels[48] = self.modestate.color

            self.lightbar_left.pixels = list(islice(self.modestate.pixels, 0, 32))
            self.lightbar_center.pixels = list(islice(self.modestate.pixels, 32, 64))
            self.lightbar_right.pixels = list(islice(self.modestate.pixels, 64, 96))


        # BEAT BASED EFFECTS
        if update_type == UpdateType.BEAT and self.mode in [Mode.DRAW_TOWARDS_RIGHT, Mode.RAINBOW_BLINK, Mode.BLINK, Mode.RANDOM_LIGHTBAR_CHANGES_COLOR, Mode.THOMAS_THE_DANK_ENGINE]:
            print(f"Beat render!")
            if self.mode == Mode.DRAW_TOWARDS_RIGHT:
                lightbar_pixel_mod = self.internal_beat_counter % 96
                if lightbar_pixel_mod < 32:
                    if lightbar_pixel_mod == 0:
                        self.current_color = generate_random_color()
                    self.lightbar_left.set_pixel(lightbar_pixel_mod, self.current_color)
                elif lightbar_pixel_mod < 64:
                    self.lightbar_center.set_pixel(lightbar_pixel_mod - 32, self.current_color)
                else:
                    self.lightbar_right.set_pixel(lightbar_pixel_mod - 64, self.current_color)
            elif self.mode == Mode.THOMAS_THE_DANK_ENGINE:
                self.lightbar_left.pixels = list(islice(self.modestate.pixels, 0, 32))
                self.lightbar_center.pixels = list(islice(self.modestate.pixels, 32, 64))
                self.lightbar_right.pixels = list(islice(self.modestate.pixels, 64, 96))
                self.modestate.pixels.rotate(1)

                return
            elif self.mode == Mode.RAINBOW_BLINK:
                for i in range(32):
                    self.lightbar_left.set_pixel(i, self.current_color)
                    self.lightbar_center.set_pixel(i, self.current_color)
                    self.lightbar_right.set_pixel(i, self.current_color)
                    self.current_color = generate_random_color()
            elif self.mode == Mode.BLINK:
                self.current_color = generate_random_color()
                for i in range(32):
                    self.lightbar_left.set_pixel(i, self.current_color)
                    self.lightbar_center.set_pixel(i, self.current_color)
                    self.lightbar_right.set_pixel(i, self.current_color)
            elif self.mode == Mode.RANDOM_LIGHTBAR_CHANGES_COLOR:
                # Handle beat frequency first.
                if self.mode.value.update_frequency == UpdateFrequency.BEAT:
                    pass
                elif UpdateFrequency.EVERY_OTHER_BEAT:
                    if self.internal_beat_counter % 2 == 1:
                        return

                # Determine which bars to update second based on the update type.
                if isinstance(self.mode.value.bar_update_type, RandomUpdateAmountOfLightbars):
                    bars_to_change = random.sample(range(3), self.mode.value.bar_update_type.amount_of_lightbars)
                    # Then perform update on those bars.
                    for bar in bars_to_change:
                        self.mode.value.lightbar_color[bar] = generate_random_color()
                        for pixel in range(len([self.lightbar_left, self.lightbar_center, self.lightbar_right][bar].pixels)):
                            [self.lightbar_left, self.lightbar_center, self.lightbar_right][bar].pixels[pixel] = self.mode.value.lightbar_color[bar]
                elif isinstance(self.mode.value.bar_update_type, OrganizedUpdateOfLightbars):
                    bars_to_change = self.mode.value.bar_update_type.lightbar_pairings[
                        self.mode.value.counter % len(self.mode.value.bar_update_type.lightbar_pairings)]
                    self.mode.value.counter += 1
                    # Then perform update on those bars.
                    if self.mode.value.bar_update_type.groups_must_have_same_color:
                        color = generate_random_color()
                        for bar in bars_to_change:
                            self.mode.value.lightbar_color[bar] = color
                            for pixel in range(
                                    len([self.lightbar_left, self.lightbar_center, self.lightbar_right][bar].pixels)):
                                [self.lightbar_left, self.lightbar_center, self.lightbar_right][bar].pixels[pixel] = self.mode.value.lightbar_color[bar]
                    else:
                        for bar in bars_to_change:
                            self.mode.value.lightbar_color[bar] = generate_random_color()
                            for pixel in range(
                                    len([self.lightbar_left, self.lightbar_center, self.lightbar_right][bar].pixels)):
                                [self.lightbar_left, self.lightbar_center, self.lightbar_right][bar].pixels[pixel] = self.mode.value.lightbar_color[bar]

        # PULSE BASED EFFECTS
        if self.mode == Mode.BEAT_SQUARE:
            if not self.pulse_effect_started:
                    self.pulse_counter = 0
                    self.direction = Direction.RIGHT
                    self.pulse_effect_started = True

            if self.pulse_effect_started:
                amount_of_pixels = 96
                updates_per_beat = 48
                step = amount_of_pixels / updates_per_beat
                pixel_positions = [
                    int(self.pulse_counter * step) % 96,
                    (int((self.pulse_counter * step) + 1) % 96),
                    (int((self.pulse_counter * step) + 2)) % 96,
                    (int((self.pulse_counter * step) + 3)) % 96,
                    (int((self.pulse_counter * step) + 4)) % 96,
                ]

                # Ensure we do not overflow
                pixel_positions = list(filter(lambda x: x < 96, pixel_positions))

                for lightbar in self.lightbar_order:
                    lightbar.clear_pixels()

                for pixel_position in pixel_positions:
                    if pixel_position < 32:
                        self.lightbar_order[0].set_pixel(pixel_position, self.current_color)
                    elif pixel_position < 64:
                        self.lightbar_order[1].set_pixel(pixel_position - 32, self.current_color)
                    else:
                        self.lightbar_order[2].set_pixel(pixel_position - 64, self.current_color)

                self.lightbar_order[0].send_to_controller(ctrl)
                self.lightbar_order[1].send_to_controller(ctrl)
                self.lightbar_order[2].send_to_controller(ctrl)
        elif self.mode == Mode.BEAT_SQUARE_BOUNCING:
            if self.pulse_effect_started == False:
                if self.pulse_counter % 24 == 0:
                    self.pulse_counter = 0
                    self.pulse_effect_started = True
                    self.direction = Direction.RIGHT
            else:
                if self.pulse_counter % 48 == 0:
                    self.direction = Direction.LEFT if self.direction == Direction.RIGHT else Direction.RIGHT
                    self.pulse_counter = 0

            if self.pulse_effect_started:
                amount_of_pixels = 96
                updates_per_beat = 48
                step = amount_of_pixels / updates_per_beat

                if self.direction == Direction.RIGHT:
                    pixel_positions = [
                        int(self.pulse_counter * step),
                        (int((self.pulse_counter * step) + 1)),
                        (int((self.pulse_counter * step) + 2)),
                        (int((self.pulse_counter * step) + 3)),
                        (int((self.pulse_counter * step) + 4)),
                    ]
                else:
                    pixel_positions = [
                        96 - (int((self.pulse_counter * step) + 4)),
                        96 - (int((self.pulse_counter * step) + 3)),
                        96 - (int((self.pulse_counter * step) + 2)),
                        96 - (int((self.pulse_counter * step) + 1)),
                        96 - (int((self.pulse_counter * step) + 0)),
                    ]

                # Ensure we do not overflow or underflow
                pixel_positions = list(filter(lambda x: x < 96, pixel_positions))
                pixel_positions = list(filter(lambda x: x >= 0, pixel_positions))

                for lightbar in self.lightbar_order:
                    lightbar.clear_pixels()

                for pixel_position in pixel_positions:
                    if pixel_position < 32:
                        self.lightbar_order[0].set_pixel(pixel_position, self.current_color)
                    elif pixel_position < 64:
                        self.lightbar_order[1].set_pixel(pixel_position - 32, self.current_color)
                    else:
                        self.lightbar_order[2].set_pixel(pixel_position - 64, self.current_color)