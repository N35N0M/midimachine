import dataclasses
import enum
import typing

from lightbar.lightbar import LightBar
from common_types import UpdateFrequency
from utils import generate_random_color

def beat_square_to_lightbar_mapping(beat_square_position: int, lightbars: typing.List[LightBar]) -> typing.List[pixels]:
    """Returns a list of pixels for each lightbar."""
    pixels = []
    for lightbar in lightbars:
        pixels.append(lightbar.pixels[beat_square_position])
    return pixels


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
    update_frequency: UpdateFrequency = UpdateFrequency.HALF_BEAT
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

class LightbarDesigner:
    def __init__(self, midi_clock, lightbar_left, lightbar_right, lightbar_center):
        self.midi_clock = midi_clock
        lightbar_left: LightBar = lightbar_left
        lightbar_center: LightBar = lightbar_center
        lightbar_right: LightBar = lightbar_right
        self.current_color = generate_random_color()
        self.mode = Mode.RAINBOW_BLINK
        self.direction = Direction.RIGHT
        self.pulse_effect_started = False
        self.lightbar_order = [self.lightbar_three, self.lightbar_two, self.lightbar]

    def set_mode(self, mode):
        self.mode = mode

    def __call__(self, event, data=None):
        if ctrl is None:
            message, delta_time = event
            if message != [248]:
                print(event)
            return
        message, deltatime = event
        if message == [248]:
            self.pulse_counter += 1
            if deltatime == 0:
                return
            pulses_per_quarter_note = 24
            bpm = 60 * (1000 / deltatime) / pulses_per_quarter_note

            # BEAT BASED EFFECTS
            if self.pulse_counter % 24 == 0:
                self.beat_number += 1
                print(f"Beat on pulse {self.pulse_counter}!")

                if self.mode == Mode.DRAW_TOWARDS_RIGHT:
                    lightbar_pixel_mod = self.beat_number % 96
                    if lightbar_pixel_mod < 32:
                        if lightbar_pixel_mod == 0:
                            self.current_color = generate_random_color()
                        self.lightbar_order[0].set_pixel(lightbar_pixel_mod, self.current_color)
                        self.lightbar_order[0].send_to_controller(ctrl)
                    elif lightbar_pixel_mod < 64:
                        self.lightbar_order[1].set_pixel(lightbar_pixel_mod - 32, self.current_color)
                        self.lightbar_order[1].send_to_controller(ctrl)
                    else:
                        self.lightbar_order[2].set_pixel(lightbar_pixel_mod - 64, self.current_color)
                        self.lightbar_order[2].send_to_controller(ctrl)
                elif self.mode == Mode.RAINBOW_BLINK:
                    for i in range(32):
                        self.lightbar.set_pixel(i, self.current_color)
                        self.lightbar_two.set_pixel(i, self.current_color)
                        self.lightbar_three.set_pixel(i, self.current_color)
                        self.current_color = generate_random_color()
                    self.lightbar.send_to_controller(ctrl)
                    self.lightbar_two.send_to_controller(ctrl)
                    self.lightbar_three.send_to_controller(ctrl)
                    ctrl.submit()
                elif self.mode == Mode.BLINK:
                    self.current_color = generate_random_color()
                    for i in range(32):
                        self.lightbar.set_pixel(i, self.current_color)
                        self.lightbar_two.set_pixel(i, self.current_color)
                        self.lightbar_three.set_pixel(i, self.current_color)
                    self.lightbar.send_to_controller(ctrl)
                    self.lightbar_two.send_to_controller(ctrl)
                    self.lightbar_three.send_to_controller(ctrl)
                elif self.mode == Mode.RANDOM_LIGHTBAR_CHANGES_COLOR:
                    # Handle beat frequency first.
                    if self.mode.value.update_frequency == UpdateFrequency.BEAT:
                        pass
                    elif UpdateFrequency.EVERY_OTHER_BEAT:
                        if self.beat_number % 2 == 1:
                            return

                    # Determine which bars to update second based on the update type.
                    if isinstance(self.mode.value.bar_update_type, RandomUpdateAmountOfLightbars):
                        bars_to_change = random.sample(range(3), self.mode.value.bar_update_type.amount_of_lightbars)
                        # Then perform update on those bars.
                        for bar in bars_to_change:
                            self.mode.value.lightbar_color[bar] = generate_random_color()
                            for pixel in self.lightbar_order[bar].pixels:
                                self.lightbar_order[bar].pixels[pixel] = self.mode.value.lightbar_color[bar]
                            self.lightbar_order[bar].send_to_controller(ctrl)
                    elif isinstance(self.mode.value.bar_update_type, OrganizedUpdateOfLightbars):
                        bars_to_change = self.mode.value.bar_update_type.lightbar_pairings[
                            self.mode.value.counter % len(self.mode.value.bar_update_type.lightbar_pairings)]
                        self.mode.value.counter += 1
                        # Then perform update on those bars.
                        if self.mode.value.bar_update_type.groups_must_have_same_color:
                            color = generate_random_color()
                            for bar in bars_to_change:
                                self.mode.value.lightbar_color[bar] = color
                                for pixel in self.lightbar_order[bar].pixels:
                                    self.lightbar_order[bar].pixels[pixel] = self.mode.value.lightbar_color[bar]
                                self.lightbar_order[bar].send_to_controller(ctrl)
                        else:
                            for bar in bars_to_change:
                                self.mode.value.lightbar_color[bar] = generate_random_color()
                                for pixel in self.lightbar_order[bar].pixels:
                                    self.lightbar_order[bar].pixels[pixel] = self.mode.value.lightbar_color[bar]
                                self.lightbar_order[bar].send_to_controller(ctrl)
                    ctrl.submit()

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

                    self.lightbar_order[0].send_to_controller(ctrl)
                    self.lightbar_order[1].send_to_controller(ctrl)
                    self.lightbar_order[2].send_to_controller(ctrl)
                    ctrl.submit()

            pass
            # print(bpm)
            # print("Clock tick!")
        elif message == [250]:
            print("MIDI clock enabled!")
            self.pulse_counter = 0
            self.direction = Direction.RIGHT
            self.pulse_effect_started = False
        elif message == [252]:
            print("MIDI clock disabled!")
            self.pulse_counter = 0
            self.direction = Direction.RIGHT
            self.pulse_effect_started = False
        else:
            print(message)