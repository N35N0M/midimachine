import dataclasses
import enum
import random
import typing

from lightbar.lightbar import LightBar
from common_types import UpdateFrequency, RgbPixel
from midi.midi_input_handler import MidiInputHandler
from utils import generate_random_color



@dataclasses.dataclass
class RandomUpdateAmountOfLightbars:
    amount_of_lightbars: int = 1

@dataclasses.dataclass
class OrganizedUpdateOfLightbars:
    lightbar_pairings: typing.List[typing.List[int]] = dataclasses.field(default_factory=lambda: [[1], [0, 2]])
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

class Mode(enum.Enum):
    DRAW_TOWARDS_RIGHT = 1
    RAINBOW_BLINK = 2
    BLINK = 3
    BEAT_SQUARE = 4
    BEAT_SQUARE_BOUNCING = 5
    RANDOM_LIGHTBAR_CHANGES_COLOR = RandomColorChangesLightBar()

class UpdateType(enum.Enum):
    PULSE = 1
    BEAT = 2

class LightbarDesigner:
    def __init__(self, midi_clock, lightbar_left, lightbar_right, lightbar_center):
        self.midi_clock: MidiInputHandler = midi_clock
        self.lightbar_left: LightBar = lightbar_left
        self.lightbar_center: LightBar = lightbar_center
        self.lightbar_right: LightBar = lightbar_right
        self.current_color = generate_random_color()
        self.mode = Mode.RANDOM_LIGHTBAR_CHANGES_COLOR
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
        # BEAT BASED EFFECTS
        if update_type == UpdateType.BEAT and self.mode in [Mode.DRAW_TOWARDS_RIGHT, Mode.RAINBOW_BLINK, Mode.BLINK, Mode.RANDOM_LIGHTBAR_CHANGES_COLOR]:
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
                if self.pulse_counter % 24 == 0:
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