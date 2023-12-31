import copy
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

purple_disco = [RgbPixel(123, 29, 175), RgbPixel(255, 47, 185)]


@dataclasses.dataclass
class RandomUpdateAmountOfLightbars:
    update_frequency: UpdateFrequency = UpdateFrequency.BEAT
    amount_of_lightbars: int = 3

@dataclasses.dataclass
class OrganizedUpdateOfLightbars:
    lightbar_pairings: typing.List[typing.List[int]] = dataclasses.field(default_factory=lambda: [[0],[1],[2]])
    color_pallette: typing.Optional[typing.Dict[int, typing.List[RgbPixel]]] = None
    update_frequency: UpdateFrequency = UpdateFrequency.BEAT
    counter = 0

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


sky = [
    RgbPixel(0, 191, 255),
    RgbPixel(0, 191, 255),
    RgbPixel(0, 191, 255),
    RgbPixel(0, 191, 255),
    RgbPixel(0, 191, 255),
    RgbPixel(0, 191, 255),
    RgbPixel(0, 191, 255),
    RgbPixel(0, 191, 255),
    RgbPixel(135, 206, 235),
    RgbPixel(135, 206, 235),
    RgbPixel(135, 206, 235),
    RgbPixel(135, 206, 235),
    RgbPixel(135, 206, 235),
    RgbPixel(135, 206, 235),
    RgbPixel(135, 206, 235),
    RgbPixel(135, 206, 235),
    RgbPixel(135, 206, 250),
    RgbPixel(135, 206, 250),
    RgbPixel(135, 206, 250),
    RgbPixel(135, 206, 250),
    RgbPixel(135, 206, 250),
    RgbPixel(135, 206, 250),
    RgbPixel(173, 216, 230),
    RgbPixel(173, 216, 230),
    RgbPixel(173, 216, 230),
    RgbPixel(173, 216, 230),
    RgbPixel(173, 216, 230),
    RgbPixel(173, 216, 230),
    RgbPixel(176, 224, 230),
    RgbPixel(176, 224, 230),
    RgbPixel(176, 224, 230),
    RgbPixel(176, 224, 230),
]

purple_sky = [
    RgbPixel(148,0,211),
    RgbPixel(148, 0, 211),
    RgbPixel(148, 0, 211),
    RgbPixel(148, 0, 211),
    RgbPixel(148, 0, 211),
    RgbPixel(148, 0, 211),
    RgbPixel(148, 0, 211),
    RgbPixel(148, 0, 211),
    RgbPixel(186, 85, 211),
    RgbPixel(186, 85, 211),
    RgbPixel(186, 85, 211),
    RgbPixel(186, 85, 211),
    RgbPixel(186, 85, 211),
    RgbPixel(186, 85, 211),
    RgbPixel(186, 85, 211),
    RgbPixel(186, 85, 211),
    RgbPixel(255,0,255),
    RgbPixel(255, 0, 255),
    RgbPixel(255, 0, 255),
    RgbPixel(255, 0, 255),
    RgbPixel(255, 0, 255),
    RgbPixel(255, 0, 255),
    RgbPixel(255, 0, 255),
    RgbPixel(255, 0, 255),
    RgbPixel(238,130,238),
    RgbPixel(238, 130, 238),
    RgbPixel(238, 130, 238),
    RgbPixel(238, 130, 238),
    RgbPixel(238, 130, 238),
    RgbPixel(238, 130, 238),
    RgbPixel(238, 130, 238),
    RgbPixel(238, 130, 238),
]

half_sun = [
    RgbPixel(255,140,0),
    RgbPixel(255,140,0),
    RgbPixel(255,140,0),
    RgbPixel(255,140,0),
    RgbPixel(255,140,0),
    RgbPixel(255,140,0),
    RgbPixel(255,165,0),
    RgbPixel(255,165,0),
    RgbPixel(255,165,0),
    RgbPixel(255,165,0),
    RgbPixel(255,165,0),
    RgbPixel(255,165,0),
    RgbPixel(255,255,102),
    RgbPixel(255,255,102),
    RgbPixel(255, 255, 0),
    RgbPixel(255, 255, 0)
]

quarter_purple_wheel = [
    RgbPixel(75,0,130),
    RgbPixel(128, 0, 128),
    RgbPixel(139,0,139),
    RgbPixel(139, 0, 139),
    RgbPixel(153,50,204),
    RgbPixel(153, 50, 204),
    RgbPixel(148,0,211),
    RgbPixel(148, 0, 211),
    RgbPixel(138,43,226),
    RgbPixel(138, 43, 226),
    RgbPixel(147,112,219),
    RgbPixel(147, 112, 219),
    RgbPixel(186,85,211),
    RgbPixel(186, 85, 211),
    RgbPixel(218,112,214),
    RgbPixel(218, 112, 214),
    RgbPixel(238,130,238),
    RgbPixel(238, 130, 238),
    RgbPixel(221,160,221),
    RgbPixel(221, 160, 221),
    RgbPixel(216,191,216),
    RgbPixel(216, 191, 216),
    RgbPixel(230,230,250),
    RgbPixel(230, 230, 250),
]

quarter_orange_wheel = [
    RgbPixel(255,127,66),
    RgbPixel(255,130,66),
    RgbPixel(255,134,66),
    RgbPixel(255,138,66),
    RgbPixel(255,143,66),
    RgbPixel(255,147,66),
    RgbPixel(255,150,66),
    RgbPixel(255,154,66),
    RgbPixel(255,158,66),
    RgbPixel(255,162,66),
    RgbPixel(255,166,66),
    RgbPixel(255,170,66),
    RgbPixel(255,174,66),
    RgbPixel(255,178,66),
    RgbPixel(255,182,66),
    RgbPixel(255,186,66),
    RgbPixel(255,190,66),
    RgbPixel(255,194,66),
    RgbPixel(255,198,66),
    RgbPixel(255,202,66),
    RgbPixel(255,221,66),
    RgbPixel(255,225,66),
    RgbPixel(255,229,66),
    RgbPixel(255,233,66),
]

@dataclasses.dataclass
class PixelSunstate:
    fade_in = True
    fade_in_counter = 0
    beat_shift = False
    beat_shift_counter = 0  # The counter == offset from centered position. max [-8, +8]
    beat_shift_direction = Direction.RIGHT
    purple_sky = False
    pixels: deque[RgbPixel] = deque(sky + half_sun + list(reversed(copy.deepcopy(half_sun))) + list(reversed(copy.deepcopy(sky))))

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

@dataclasses.dataclass
class BeatSquareBounceState:
    color: RgbPixel = RgbPixel(255, 0, 0)
    width: typing.Final[int] = 4
    pulse_velocity: int = 4
    direction: Direction = Direction.RIGHT
    pixels: deque[RgbPixel] = deque([RgbPixel(0, 0, 0) for _ in range(64)])
    beat_synced = False

@dataclasses.dataclass
class ColorwaveState:
    beat_interval = 1
    previous_color: RgbPixel = RgbPixel(0, 0, 0)
    colour_pallette: list[RgbPixel] = dataclasses.field(default_factory=lambda: [RgbPixel(255, 0, 0), RgbPixel(0, 255, 0), RgbPixel(0, 0, 255)])
    pixels: list[RgbPixel] = dataclasses.field(default_factory=lambda: list([RgbPixel(0, 0, 0) for _ in range(96)]))

class Mode(enum.Enum):
    DRAW_TOWARDS_RIGHT = 1
    RAINBOW_BLINK = 2
    BLINK = 3
    BEAT_SQUARE = 4
    BEAT_SQUARE_BOUNCING = 5
    LIGHTBARS_CHANGE_COLOR = 6
    THOMAS_THE_DANK_ENGINE = 7
    RETROWAVE_GRID = 8
    OFF = 9
    NOOT_NOOT = 10
    PIXEL_SUN = 11
    COLOR_WHEEL = 12
    COLOR_WAVE = 13

disco_pallette = [
    RgbPixel(15, 192, 252),
    RgbPixel(123, 29, 175),
    RgbPixel(255, 47, 185),
    RgbPixel(212, 255, 71),
    RgbPixel(27, 54, 73),
]

@dataclasses.dataclass
class ColorWheelState:
    """
    Divide the strip in two. Each strip has two mirrored color ranges that are identical but mirrored.
    Rotate both halves evenly to get a cool effect!
    """
    pixels: list[RgbPixel] = dataclasses.field(default_factory=lambda: quarter_purple_wheel + list(reversed(quarter_purple_wheel)) + quarter_purple_wheel + list(reversed(quarter_purple_wheel)))

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
        self.mode = Mode.LIGHTBARS_CHANGE_COLOR
        self.modestate:  typing.Union[TankEngineState, RetrowaveGridState, None] = None
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
        current_track = self.traktor_metadata.current_track_deck_a if self.traktor_metadata.master_deck == "A" else self.traktor_metadata.current_track_deck_b
        current_track_elapsed = self.traktor_metadata.current_track_elapsed_deck_a if self.traktor_metadata.master_deck == "A" else self.traktor_metadata.current_track_elapsed_deck_b
        if current_track == "Junkyard Dunebuggy":
            if (29 < current_track_elapsed < 48) or (77 < current_track_elapsed < 95.8):
                self.mode = Mode.COLOR_WHEEL
                if not isinstance(self.modestate, ColorWheelState):
                    self.modestate = ColorWheelState()
                    self.modestate.pixels = quarter_orange_wheel + list(reversed(quarter_orange_wheel)) + quarter_orange_wheel + list(reversed(quarter_orange_wheel))
            elif (0 < current_track_elapsed < 95.8) or (172.8 < current_track_elapsed < 182.2):
                self.mode = Mode.LIGHTBARS_CHANGE_COLOR
                if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                    self.modestate = OrganizedUpdateOfLightbars()
                self.modestate.color_pallette = {
                    0: [RgbPixel(255,140,0), RgbPixel(255,215,0)],
                    1: [RgbPixel(255,140,0), RgbPixel(255,215,0)],
                    2: [RgbPixel(255,140,0), RgbPixel(255,215,0)],
                }
                self.modestate.lightbar_pairings = [[0, 2], [1]]
            elif (95.8 < current_track_elapsed < 172.8):
                self.mode = Mode.PIXEL_SUN
                if not isinstance(self.modestate, PixelSunstate):
                    self.modestate = PixelSunstate()
                self.modestate.purple_sky = False
                self.modestate.beat_shift = True
                self.modestate.fade_in = False
            elif (182.2 < current_track_elapsed < 220):
                self.mode = Mode.PIXEL_SUN
                if not isinstance(self.modestate, PixelSunstate):
                    self.modestate = PixelSunstate()
                self.modestate.purple_sky = True
                self.modestate.beat_shift = True
                self.modestate.fade_in = False
            else:
                self.mode = Mode.OFF
                self.modestate = None
        elif current_track == "Disco Guy (Original Version)":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR

            if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                self.modestate = OrganizedUpdateOfLightbars()
            self.modestate.color_pallette = {
                0: purple_disco,
                1: purple_disco,
                2: purple_disco,
            }
            self.modestate.lightbar_pairings = [[0, 2], [1]]
        elif current_track == "Skibidi (Romantic Edition)":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR

            if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                self.modestate = OrganizedUpdateOfLightbars()
            self.modestate.color_pallette = {
                0: purple_disco,
                1: purple_disco,
                2: purple_disco,
            }
            self.modestate.lightbar_pairings = [[0, 2], [1]]
        elif current_track == "Don't Leave Me Lonely (feat. YEBBA) [Purple Disco Machine Remix]":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR

            if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                self.modestate = OrganizedUpdateOfLightbars()
            self.modestate.color_pallette = {
                0: disco_pallette,
                1: disco_pallette,
                2: disco_pallette,
            }
            self.modestate.lightbar_pairings = [[0, 2], [1]]
        elif current_track == "Disco Inferno":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR

            if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                self.modestate = OrganizedUpdateOfLightbars()
            self.modestate.color_pallette = {
                0: disco_pallette,
                1: disco_pallette,
                2: disco_pallette,
            }
            self.modestate.lightbar_pairings = [[0, 2], [1]]
        elif current_track == "Cha Cha Cha":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR

            if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                self.modestate = OrganizedUpdateOfLightbars()

            pallette = [RgbPixel(255,20,147), RgbPixel(0,255,0)]
            self.modestate.color_pallette = {
                0: pallette,
                1: pallette,
                2: pallette,
            }
            self.modestate.lightbar_pairings = [[0, 2], [1]]
        elif current_track == "Voodoo? (Lazywax Remix)":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR

            if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                self.modestate = OrganizedUpdateOfLightbars()
            self.modestate.color_pallette = {
                0: disco_pallette,
                1: disco_pallette,
                2: disco_pallette,
            }
            self.modestate.lightbar_pairings = [[0, 2], [1]]
        elif current_track == "City Boy":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR
            self.modestate = RandomUpdateAmountOfLightbars()
        elif current_track == "They're Taking The Hobbits To Isengard":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR
            self.modestate = RandomUpdateAmountOfLightbars()
        elif current_track == "Bezos I":
            if current_track_elapsed > 42:
                self.mode = Mode.LIGHTBARS_CHANGE_COLOR
                self.modestate = RandomUpdateAmountOfLightbars()
            else:
                self.mode = Mode.LIGHTBARS_CHANGE_COLOR
                if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                    self.modestate = OrganizedUpdateOfLightbars()
                self.modestate.color_pallette = {
                    0: [RgbPixel(255, 153, 0), RgbPixel(0,0,0)],
                    1: [RgbPixel(255, 153, 0), RgbPixel(0,0,0)],
                    2: [RgbPixel(255, 153, 0), RgbPixel(0,0,0)],
                }
                self.modestate.lightbar_pairings = [[0, 2], [1]]

                if 7.2 < current_track_elapsed < 7.9:
                    self.modestate.update_frequency = UpdateFrequency.HALF_BEAT
                elif 15.5 < current_track_elapsed < 16.3:
                    self.modestate.update_frequency = UpdateFrequency.HALF_BEAT
                elif 24.1 < current_track_elapsed < 24.9:
                    self.modestate.update_frequency = UpdateFrequency.HALF_BEAT
                elif 7.9 < current_track_elapsed < 8.3:
                    return
                elif 16.4 < current_track_elapsed < 16.7:
                    return
                elif 25 < current_track_elapsed < 25.3:
                    return
                else:
                    self.modestate.update_frequency = UpdateFrequency.BEAT
        elif current_track == "Keep Moving":
            if 132.2 < current_track_elapsed < 149.4:
                self.mode = Mode.COLOR_WAVE
                if not isinstance(self.modestate, ColorwaveState):
                    self.modestate = ColorwaveState()
                    self.modestate.colour_pallette = [RgbPixel(219, 172, 52), RgbPixel(226, 88, 37)]
                    self.modestate.beat_interval = 2
            elif current_track_elapsed > 28.5:
                self.mode = Mode.LIGHTBARS_CHANGE_COLOR
                if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                    self.modestate = OrganizedUpdateOfLightbars()
                self.modestate.color_pallette = {
                    0: [RgbPixel(219, 172, 52), RgbPixel(226, 88, 37)],
                    1: [RgbPixel(219, 172, 52), RgbPixel(226, 88, 37)],
                    2: [RgbPixel(219, 172, 52), RgbPixel(226, 88, 37)],
                }
                self.modestate.lightbar_pairings = [[0, 2], [1]]
            else:
                self.mode = Mode.OFF
                self.modestate = None
        elif current_track == "Paris (Aeroplane Remix)":
            if 0 < current_track_elapsed <= 34.5:
                self.mode = Mode.RETROWAVE_GRID
                if not isinstance(self.modestate, RetrowaveGridState):
                    self.modestate = RetrowaveGridState()
                    self.modestate.colour_pallette = [generate_random_color(), generate_random_color()]
                    self.modestate.beat_interval = 2
            elif current_track_elapsed > 34.5:
                self.mode = Mode.COLOR_WAVE
                if not isinstance(self.modestate, ColorwaveState):
                    self.modestate = ColorwaveState()
                    self.modestate.colour_pallette = [generate_random_color(), generate_random_color()]
                    self.modestate.beat_interval = 1
            else:
                self.mode = Mode.OFF
                self.modestate = None
        elif current_track == "Hot":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR
            self.modestate = RandomUpdateAmountOfLightbars()

        elif current_track == "We Don't Need Another Hero (Thunderdome)":
            if (0 < current_track_elapsed < 73.8) or \
                (92.5 < current_track_elapsed < 149) or \
                    (204 < current_track_elapsed < 238):
                self.mode = Mode.LIGHTBARS_CHANGE_COLOR
                if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                    self.modestate = OrganizedUpdateOfLightbars()
                self.modestate.color_pallette = {
                    0: [RgbPixel(255, 0, 0), RgbPixel(150, 0, 0)],
                    1: [RgbPixel(0, 255, 0), RgbPixel(0, 150, 0)],
                    2: [RgbPixel(255, 0, 0), RgbPixel(150, 0, 0)],
                }
                self.modestate.lightbar_pairings = [[0, 2], [1]]
            elif (73.8 < current_track_elapsed < 92.5) or \
                    (149 < current_track_elapsed < 182):
                self.mode = Mode.LIGHTBARS_CHANGE_COLOR
                if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                    self.modestate = OrganizedUpdateOfLightbars()
                self.modestate.color_pallette = {
                    0: [RgbPixel(50,205,50), RgbPixel(0,255,0)],  #limegreens
                    1: [RgbPixel(135,206,235), RgbPixel(30,144,255)], #skyblues
                    2: [RgbPixel(50,205,50), RgbPixel(0,255,0)],  #limegreens
                }
            elif (185.3 < current_track_elapsed < 204):
                self.mode = Mode.PIXEL_SUN
                if not isinstance(self.modestate, PixelSunstate):
                    self.modestate = PixelSunstate()
                self.modestate.purple_sky = False
                self.modestate.beat_shift = True
                self.modestate.fade_in = False
            else:
                self.mode = Mode.OFF
        elif current_track == "Lost Woods":
            self.mode = Mode.COLOR_WHEEL
            if not isinstance(self.modestate, ColorWheelState):
                self.modestate = ColorWheelState()
        elif current_track == "Biggie smalls the tank engine":
            if current_track_elapsed > 20.8:
                self.mode = Mode.THOMAS_THE_DANK_ENGINE
                self.modestate = TankEngineState()
            else:
                self.mode = Mode.OFF
                self.modestate = None
        elif current_track == "Hard to Be Funky (feat. Lou Hayter)":
            self.mode = Mode.RETROWAVE_GRID
            if not isinstance(self.modestate, RetrowaveGridState):
                self.modestate = RetrowaveGridState()
            if not self.lightbar_center.pixels[16] == self.modestate.color:
                self.modestate.color = generate_random_color()
        elif current_track == "Noot noot the police":
            if current_track_elapsed > 1.9:
                self.mode = Mode.NOOT_NOOT
                if not isinstance(self.modestate, NootNootState) and update_type == UpdateType.BEAT:
                    self.modestate = NootNootState()
            else:
                self.mode = Mode.OFF
                self.modestate = None
        elif current_track == "Milestones":
            # self.mode = Mode.RETROWAVE_GRID
            # if not isinstance(self.modestate, RetrowaveGridState):
            #     self.modestate = RetrowaveGridState()
            self.mode = Mode.COLOR_WAVE
            if not isinstance(self.modestate, ColorwaveState):
                self.modestate = ColorwaveState()

            if current_track_elapsed > 69.7:
                self.modestate.beat_interval = 1
            else:
                self.modestate.beat_interval = 2
        elif current_track == "10 Years (Chromeo Remix)":
            self.mode = Mode.COLOR_WAVE
            if not isinstance(self.modestate, ColorwaveState):
                self.modestate = ColorwaveState()
            self.modestate.colour_pallette = [RgbPixel(34,139,34), RgbPixel(0,255,0)]
        elif current_track == "The Girl and the Robot":
            if current_track_elapsed > 222:
                self.mode = Mode.OFF
                self.modestate = None
            else:
                self.mode = Mode.RETROWAVE_GRID
                if not isinstance(self.modestate, RetrowaveGridState):
                    self.modestate = RetrowaveGridState()
        elif current_track == "Make Me Thomas (feat. Jawn Legend)":
            self.mode = Mode.THOMAS_THE_DANK_ENGINE
            self.modestate = TankEngineState()
        elif current_track == "Santa Catarina":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR
            if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                self.modestate = OrganizedUpdateOfLightbars()
            self.modestate.color_pallette = {
                0: disco_pallette,  # limegreens
                1: disco_pallette,  # skyblues
                2: disco_pallette,  # limegreens
            }
        elif current_track == "Rasputin":
            self.mode = Mode.LIGHTBARS_CHANGE_COLOR
            if not isinstance(self.modestate, OrganizedUpdateOfLightbars):
                self.modestate = OrganizedUpdateOfLightbars()
            self.modestate.color_pallette = {
                0: disco_pallette,  # limegreens
                1: disco_pallette,  # skyblues
                2: disco_pallette,  # limegreens
            }
        elif current_track == "Crescendolls":
            self.mode = Mode.RETROWAVE_GRID
            if not isinstance(self.modestate, RetrowaveGridState):
                self.modestate = RetrowaveGridState()
            if not self.lightbar_center.pixels[16] == self.modestate.color:
                self.modestate.color = generate_random_color()
        elif current_track == "Time Machine":
            self.mode = Mode.RETROWAVE_GRID
            if not isinstance(self.modestate, RetrowaveGridState):
                self.modestate = RetrowaveGridState()
            if not self.lightbar_center.pixels[16] == self.modestate.color:
                self.modestate.color = generate_random_color()
        elif current_track == "Jeg Vil Bare Danse":
            self.mode = Mode.COLOR_WAVE
            if not isinstance(self.modestate, ColorwaveState):
                self.modestate = ColorwaveState()
            self.modestate.colour_pallette = disco_pallette

            if 52.4 < current_track_elapsed < 84.5:
                self.modestate.beat_interval = 1
            elif 134.5 < current_track_elapsed < 167:
                self.modestate.beat_interval = 1
            else:
                self.modestate.beat_interval = 2
        elif current_track == "Amberina Sun":
            self.mode = Mode.PIXEL_SUN

            if not isinstance(self.modestate, PixelSunstate):
                self.modestate = PixelSunstate()
                self.lightbar_left.pixels = [RgbPixel(0, 0, 0) for _ in range(32)]
                self.lightbar_center.pixels = [RgbPixel(0, 0, 0) for _ in range(32)]
                self.lightbar_right.pixels = [RgbPixel(0, 0, 0) for _ in range(32)]

            if 146.0 < current_track_elapsed < 249.5:
                self.modestate.purple_sky = True
            else:
                self.modestate.purple_sky = False

            if 0 < current_track_elapsed < 41.5:
                self.modestate.fade_in = True
            elif 41.5 < current_track_elapsed:
                self.modestate.fade_in = False
                self.modestate.fade_in_counter = 0
                self.modestate.beat_shift = True
            else:
                self.modestate.fade_in_counter = 0
                self.modestate.fade_in = False
        elif current_track == "Mopedbart":
            self.mode = Mode.PIXEL_SUN

            if not isinstance(self.modestate, PixelSunstate):
                self.modestate = PixelSunstate()
                self.lightbar_left.pixels = [RgbPixel(0, 0, 0) for _ in range(32)]
                self.lightbar_center.pixels = [RgbPixel(0, 0, 0) for _ in range(32)]
                self.lightbar_right.pixels = [RgbPixel(0, 0, 0) for _ in range(32)]

            self.modestate.purple_sky = True

            if 0 < current_track_elapsed < 36:
                self.modestate.fade_in = True
            else:
                self.modestate.fade_in = False
                self.modestate.fade_in_counter = 0
                self.modestate.beat_shift = True
        else:
            # Select a random (good) effect for random song.
            if not self.traktor_metadata.master_deck_change_handled:
                random_mode = random.sample([Mode.COLOR_WAVE, Mode.RETROWAVE_GRID, Mode.LIGHTBARS_CHANGE_COLOR], 1)[0]
                self.mode = random_mode
                if random_mode == Mode.COLOR_WAVE:
                    self.modestate = ColorwaveState()
                    self.modestate.beat_interval = 2
                    self.modestate.colour_pallette = [generate_random_color(), generate_random_color(), generate_random_color()]
                elif random_mode == Mode.PIXEL_SUN:
                    self.modestate = PixelSunstate()
                    self.modestate.beat_shift = True
                    self.modestate.fade_in = False
                elif random_mode == Mode.RETROWAVE_GRID:
                    self.modestate = RetrowaveGridState()
                elif random_mode == Mode.LIGHTBARS_CHANGE_COLOR:
                    self.modestate = OrganizedUpdateOfLightbars()
                    random_color_pallete_one = [generate_random_color(), generate_random_color(), generate_random_color()]
                    random_color_pallete_two = [generate_random_color(), generate_random_color(), generate_random_color()]
                    self.modestate.color_pallette = {
                        0: random_color_pallete_one,
                        1: random_color_pallete_two,
                        2: random_color_pallete_one,
                    }
                    self.modestate.lightbar_pairings = [[0,2], [1]]
                self.traktor_metadata.master_deck_change_handled = True

            if self.mode == Mode.RETROWAVE_GRID:
                # There is a bug where the color spawn changes color before it shifts.
                # But the whole effect is in fact a bug, so it's fine.
                if not self.lightbar_center.pixels[16] == self.modestate.color:
                    self.modestate.color = generate_random_color()


        if self.mode == Mode.COLOR_WAVE and isinstance(self.modestate, ColorwaveState):
            new_color = self.modestate.previous_color

            # Always copy a pixel on a beat
            if self.internal_pulse_counter % 1 == 0:
                for i in range(0, 47):
                    self.modestate.pixels[i] = self.modestate.pixels[i + 1]
                for i in range(95, 48, -1):
                    self.modestate.pixels[i] = self.modestate.pixels[i-1]

            if self.internal_beat_counter % self.modestate.beat_interval == 0 and update_type == UpdateType.BEAT:

                while new_color == self.modestate.previous_color:
                    new_color = random.sample(self.modestate.colour_pallette, 1)[0]
                self.modestate.previous_color = new_color
                self.modestate.pixels[47] = new_color
                self.modestate.pixels[48] = new_color

            self.lightbar_left.pixels = self.modestate.pixels[0:32]
            self.lightbar_center.pixels = self.modestate.pixels[32:64]
            self.lightbar_right.pixels = self.modestate.pixels[64:96]
            return



        if self.mode == Mode.PIXEL_SUN and isinstance(self.modestate, PixelSunstate):
            """
            The middle light bar is a sun.
            The left and right light bars are the clouds.
            """

            if update_type == UpdateType.BEAT:
                if self.modestate.purple_sky:
                    self.modestate.pixels = deque(purple_sky + half_sun + list(reversed(copy.deepcopy(half_sun))) + list(reversed(copy.deepcopy(purple_sky))))
                    self.modestate.pixels.rotate(self.modestate.beat_shift_counter)
                else:
                    self.modestate.pixels = deque(sky + half_sun + list(reversed(copy.deepcopy(half_sun))) + list(reversed(copy.deepcopy(sky))))
                    self.modestate.pixels.rotate(self.modestate.beat_shift_counter)

                if self.modestate.fade_in:
                    lightbar_left_pixels = copy.deepcopy(list(islice(self.modestate.pixels, 0, 32)))
                    lightbar_center_pixels = copy.deepcopy(list(islice(self.modestate.pixels, 32, 64)))
                    lightbar_right_pixels = copy.deepcopy(list(islice(self.modestate.pixels, 64, 96)))

                    if self.modestate.fade_in_counter <= 32:
                        self.lightbar_left.pixels = lightbar_left_pixels[0:self.modestate.fade_in_counter] + [RgbPixel(0, 0, 0)] * (32 - self.modestate.fade_in_counter)
                        self.lightbar_right.pixels = list(reversed(self.lightbar_left.pixels))
                        self.lightbar_center.pixels = [RgbPixel(0, 0, 0) for _ in range(32)]
                    elif 32 < self.modestate.fade_in_counter < 32+17:
                        counter = self.modestate.fade_in_counter - 32
                        half_the_sun = lightbar_center_pixels[0:counter] + [RgbPixel(0, 0, 0)] * (16 - counter)
                        self.lightbar_center.pixels = half_the_sun + list(reversed(half_the_sun))

                    self.modestate.fade_in_counter += 1
                else:
                    self.lightbar_left.pixels = list(islice(self.modestate.pixels, 0, 32))
                    self.lightbar_center.pixels = list(islice(self.modestate.pixels, 32, 64))
                    self.lightbar_right.pixels = list(islice(self.modestate.pixels, 64, 96))

                if self.modestate.beat_shift:
                    if self.modestate.beat_shift_direction == Direction.RIGHT:
                        self.modestate.beat_shift_counter += 1
                    elif self.modestate.beat_shift_direction == Direction.LEFT:
                        self.modestate.beat_shift_counter -= 1

                    if self.modestate.beat_shift_counter % 8 == 0 and self.modestate.beat_shift_counter != 0:
                        if self.modestate.beat_shift_direction == Direction.RIGHT:
                            self.modestate.beat_shift_direction = Direction.LEFT
                        elif self.modestate.beat_shift_direction == Direction.LEFT:
                            self.modestate.beat_shift_direction = Direction.RIGHT

            return


        if self.mode == Mode.COLOR_WHEEL and isinstance(self.modestate, ColorWheelState):
            left_half = deque(self.modestate.pixels[0:48])
            right_half = deque(self.modestate.pixels[48:96])

            left_half.rotate(-1)
            right_half.rotate(1)

            self.modestate.pixels = list(left_half) + list(right_half)

            self.lightbar_left.pixels = self.modestate.pixels[0:32]
            self.lightbar_center.pixels = self.modestate.pixels[32:64]
            self.lightbar_right.pixels = self.modestate.pixels[64:96]
            return

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
        if self.mode == Mode.THOMAS_THE_DANK_ENGINE and update_type == UpdateType.BEAT:
            self.lightbar_left.pixels = list(islice(self.modestate.pixels, 0, 32))
            self.lightbar_center.pixels = list(islice(self.modestate.pixels, 32, 64))
            self.lightbar_right.pixels = list(islice(self.modestate.pixels, 64, 96))
            self.modestate.pixels.rotate(1)

            return
        if self.mode == Mode.RAINBOW_BLINK:
            for i in range(32):
                self.lightbar_left.set_pixel(i, self.current_color)
                self.lightbar_center.set_pixel(i, self.current_color)
                self.lightbar_right.set_pixel(i, self.current_color)
                self.current_color = generate_random_color()
        if self.mode == Mode.BLINK:
            self.current_color = generate_random_color()
            for i in range(32):
                self.lightbar_left.set_pixel(i, self.current_color)
                self.lightbar_center.set_pixel(i, self.current_color)
                self.lightbar_right.set_pixel(i, self.current_color)

        if self.mode == Mode.LIGHTBARS_CHANGE_COLOR and (isinstance(self.modestate, OrganizedUpdateOfLightbars) or isinstance(self.modestate, RandomUpdateAmountOfLightbars)):
            # Handle beat frequency first.
            if not update_type == UpdateType.BEAT and self.modestate.update_frequency == UpdateFrequency.BEAT:
                return
            elif not self.internal_pulse_counter % 12 == 0 and self.modestate.update_frequency == UpdateFrequency.HALF_BEAT:
                return

            # Determine which bars to update second based on the update type.
            if isinstance(self.modestate, RandomUpdateAmountOfLightbars):
                bars_to_change = random.sample(range(3), self.modestate.amount_of_lightbars)
                # Then perform update on those bars.
                for bar in bars_to_change:
                    for pixel in range(len([self.lightbar_left, self.lightbar_center, self.lightbar_right][bar].pixels)):
                        [self.lightbar_left, self.lightbar_center, self.lightbar_right][bar].pixels[pixel] = generate_random_color()
            if isinstance(self.modestate, OrganizedUpdateOfLightbars):
                bars_to_change = self.modestate.lightbar_pairings[
                    self.modestate.counter % len(self.modestate.lightbar_pairings)]
                self.modestate.counter += 1
                # Then perform update on those bars.
                print(bars_to_change)
                previous_color = [self.lightbar_left, self.lightbar_center, self.lightbar_right][bars_to_change[0]].pixels[0]

                if self.modestate.color_pallette is not None and bars_to_change[0] in self.modestate.color_pallette:
                    color_to_set = previous_color
                    while color_to_set == previous_color:
                        color_to_set = random.sample(self.modestate.color_pallette[bars_to_change[0]], 1)[0]
                else:
                    color_to_set = generate_random_color()
                for bar in bars_to_change:
                    for pixel in range(
                            len([self.lightbar_left, self.lightbar_center, self.lightbar_right][bar].pixels)):
                        [self.lightbar_left, self.lightbar_center, self.lightbar_right][bar].pixels[pixel] = color_to_set

        if self.mode == Mode.BEAT_SQUARE:
            if not self.pulse_effect_started:
                    self.internal_pulse_counter = 0
                    self.direction = Direction.RIGHT
                    self.pulse_effect_started = True

            if self.pulse_effect_started:
                amount_of_pixels = 96
                updates_per_beat = 48
                step = amount_of_pixels / updates_per_beat
                pixel_positions = [
                    int(self.internal_pulse_counter * step) % 96,
                    (int((self.internal_pulse_counter * step) + 1) % 96),
                    (int((self.internal_pulse_counter * step) + 2)) % 96,
                    (int((self.internal_pulse_counter * step) + 3)) % 96,
                    (int((self.internal_pulse_counter * step) + 4)) % 96,
                ]

                # Ensure we do not overflow
                pixel_positions = list(filter(lambda x: x < 96, pixel_positions))

                for lightbar in [self.lightbar_left, self.lightbar_center, self.lightbar_right]:
                    lightbar.clear_pixels()

                for pixel_position in pixel_positions:
                    if pixel_position < 32:
                        self.lightbar_left.set_pixel(pixel_position, self.current_color)
                    elif pixel_position < 64:
                        self.lightbar_center.set_pixel(pixel_position - 32, self.current_color)
                    else:
                        self.lightbar_right.set_pixel(pixel_position - 64, self.current_color)

        if self.mode == Mode.BEAT_SQUARE_BOUNCING:
            if update_type == UpdateType.BEAT:
                self.modestate.beat_synced = True

            if self.modestate.beat_synced:

                if self.modestate.direction == Direction.RIGHT and self.internal_pulse_counter % 96 == 0:
                    self.modestate.direction = Direction.LEFT
                    self.modestate.pixels = deque(
                        [self.modestate.color for _ in range(self.modestate.width)] + [RgbPixel(0, 0, 0) for _ in
                                                                                   range(96 - self.modestate.width)])

                elif self.modestate.direction == Direction.LEFT and self.internal_pulse_counter % 96 == 0:
                    self.modestate.direction = Direction.RIGHT
                    self.modestate.pixels = deque(
                        [RgbPixel(0, 0, 0) for _ in range(96 - self.modestate.width)] + [self.modestate.color for _ in range(self.modestate.width)])


                # Move according to velocity.
                if self.modestate.direction == Direction.RIGHT:
                    self.modestate.pixels.rotate(1)
                else:
                    self.modestate.pixels.rotate(-1)

                # Render
                self.lightbar_left.pixels = list(islice(self.modestate.pixels, 0, 32))
                self.lightbar_center.pixels = list(islice(self.modestate.pixels, 32, 64))
                self.lightbar_right.pixels = list(islice(self.modestate.pixels, 64, 96))




