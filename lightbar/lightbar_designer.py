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
    pixels: list[RgbPixel] = dataclasses.field(default_factory = lambda: [RgbPixel(0, 0, 0) for _ in range(96)])

@dataclasses.dataclass
class NootNootState:
    pulse_counter = 0


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
                                    ] + [RgbPixel(0, 0, 0) for _ in range(35)] +
                                    [
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
                                    ]

                                    + [RgbPixel(0, 0, 0) for _ in range(36)])

class Mode(enum.Enum):
    DRAW_TOWARDS_RIGHT = 1
    RAINBOW_BLINK = 2
    BLINK = 3
    BEAT_SQUARE = 4
    BEAT_SQUARE_BOUNCING = 5
    RANDOM_LIGHTBAR_CHANGES_COLOR = RandomColorChangesLightBar()
    THOMAS_THE_DANK_ENGINE = 7
    RETROWAVE_GRID = 8
    OFF = 9
    NOOT_NOOT = 10

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
            if self.traktor_metadata.current_track_elapsed_deck_a > 20.8:
                self.mode = Mode.THOMAS_THE_DANK_ENGINE
                self.modestate = TankEngineState()
            else:
                self.mode = Mode.OFF
        if self.traktor_metadata.current_track_deck_a == "Noot noot the police":
            if self.traktor_metadata.current_track_elapsed_deck_a > 1.9:
                self.mode = Mode.NOOT_NOOT
                if not isinstance(self.modestate, NootNootState) and update_type == UpdateType.BEAT:
                    self.modestate = NootNootState()
            else:
                self.mode = Mode.OFF
                self.modestate = None
        if self.traktor_metadata.current_track_deck_a == "The Girl and the Robot":
            if self.traktor_metadata.current_track_elapsed_deck_a > 222:
                self.mode = Mode.OFF
            else:
                self.mode = Mode.RETROWAVE_GRID
                if not isinstance(self.modestate, RetrowaveGridState):
                    self.modestate = RetrowaveGridState()
        if self.traktor_metadata.current_track_deck_a == "Make Me Thomas (feat. Jawn Legend)":
            self.mode = Mode.THOMAS_THE_DANK_ENGINE
            self.modestate = TankEngineState()

        if self.mode == Mode.NOOT_NOOT and isinstance(self.modestate, NootNootState):
            # One noot happens during a half beat.
            # So we have 12 pulses to use.
            # Six pulses out, six pulses in.
            # So 32 pixels/six pulses gives us max five pixels at a time.
            def nootbar(lightbar: LightBar, direction: Direction.RIGHT):
                orange_pixel = RgbPixel(237, 112, 20)
                black_pixel = RgbPixel(0, 0, 0)

                mod_96 = self.modestate.pulse_counter % 96

                if direction == direction.LEFT:
                    lightbar.pixels.reverse()

                if 0 <= mod_96 <= 4:
                    lightbar.pixels[mod_96*5 + 0] = orange_pixel
                    lightbar.pixels[mod_96*5 + 1] = orange_pixel
                    lightbar.pixels[mod_96*5 + 2] = orange_pixel
                    lightbar.pixels[mod_96*5 + 3] = orange_pixel
                    lightbar.pixels[mod_96*5 + 4] = orange_pixel
                elif 5 <= mod_96 <= 9:
                    step_size = 9 - mod_96  # 4, 3, 2, 1, 0
                    lightbar.pixels[step_size*5 + 0] = black_pixel
                    lightbar.pixels[step_size*5 + 1] = black_pixel
                    lightbar.pixels[step_size*5 + 2] = black_pixel
                    lightbar.pixels[step_size*5 + 3] = black_pixel
                    lightbar.pixels[step_size*5 + 4] = black_pixel
                elif 20 <= mod_96 <= 25:
                    mod_96 -= 20
                    lightbar.pixels[mod_96*5 + 0] = orange_pixel
                    lightbar.pixels[mod_96*5 + 1] = orange_pixel
                    lightbar.pixels[mod_96*5 + 2] = orange_pixel
                    lightbar.pixels[mod_96*5 + 3] = orange_pixel
                    lightbar.pixels[mod_96*5 + 4] = orange_pixel
                elif 26 <= mod_96 <= 31:
                    step_size = 31 - mod_96  # 4, 3, 2, 1, 0
                    lightbar.pixels[step_size * 5 + 0] = black_pixel
                    lightbar.pixels[step_size * 5 + 1] = black_pixel
                    lightbar.pixels[step_size * 5 + 2] = black_pixel
                    lightbar.pixels[step_size * 5 + 3] = black_pixel
                    lightbar.pixels[step_size * 5 + 4] = black_pixel

                if direction == direction.LEFT:
                    lightbar.pixels.reverse()

            nootbar(self.lightbar_left, Direction.LEFT)
            nootbar(self.lightbar_right, Direction.RIGHT)

            if 36 < (self.modestate.pulse_counter % 96) < 96:
                def calculate_blue_light(pixel_pos: int, mod_pulse_22: int):
                    if mod_pulse_22 < 11:
                        return RgbPixel(0, 0,
                                                                  (255 // 11) * ((mod_pulse_22 + pixel_pos) % 11))
                    else:
                        return RgbPixel(0, 0, 255 - (255 // 11) * (
                            (mod_pulse_22 + pixel_pos) % 11))

                def calculate_red_light(pixel_pos: int, mod_pulse_22: int):
                    if mod_pulse_22 < 11:
                        return RgbPixel((255 // 11) * ((mod_pulse_22 + pixel_pos) % 11), 0, 0)
                    else:
                        return RgbPixel(255 - (255 // 11) * ((mod_pulse_22 + pixel_pos) % 11), 0, 0)

                for i in range(0, 32):
                    self.lightbar_left.pixels[i] = RgbPixel(0, 0, 0)
                    self.lightbar_right.pixels[i] = RgbPixel(0, 0, 0)


                for i in range(0, 16):
                    self.lightbar_center.pixels[i] = calculate_blue_light(i, self.modestate.pulse_counter % 22)

                for i in range(16, 32):
                    self.lightbar_center.pixels[i] = calculate_red_light(i, self.modestate.pulse_counter % 22)
            else:
                self.lightbar_center.pixels = [RgbPixel(0, 0, 0)] * 32

            if update_type == UpdateType.PULSE:
                self.modestate.pulse_counter+=1

            return




        if self.mode == Mode.RETROWAVE_GRID:
            # First, shift all the current pixels outwards.
            pulse_count = self.internal_pulse_counter % 48

            if pulse_count != 0:
                if pulse_count % 2 == 0:
                    pulse_count = pulse_count // 2
                    pulse_count = pulse_count - 1
                    left_side = self.modestate.pixels[0:(48-pulse_count)]
                    right_side = self.modestate.pixels[(48+pulse_count):96]
                    middle = self.modestate.pixels[(48-pulse_count):(48+pulse_count)]
                    left_side = left_side[1:] + [RgbPixel(0, 0, 0)]
                    right_side = [RgbPixel(0, 0, 0)] + right_side[:-1]
                    self.modestate.pixels = left_side + middle + right_side


            if self.internal_pulse_counter % 24 == 0:
                # Spawn a new pixel on every beat.
                self.modestate.pixels[47] = self.modestate.color
                self.modestate.pixels[48] = self.modestate.color

            self.lightbar_left.pixels = list(islice(self.modestate.pixels, 0, 32))
            self.lightbar_center.pixels = list(islice(self.modestate.pixels, 32, 64))
            self.lightbar_right.pixels = list(islice(self.modestate.pixels, 64, 96))
            return

        if self.mode == Mode.OFF:
            self.lightbar_left.pixels = [RgbPixel(0, 0, 0) for _ in range(32)]
            self.lightbar_center.pixels = [RgbPixel(0, 0, 0) for _ in range(32)]
            self.lightbar_right.pixels = [RgbPixel(0, 0, 0) for _ in range(32)]

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