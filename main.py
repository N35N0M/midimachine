
from __future__ import print_function

import dataclasses
import enum
import logging
import random
import sys
import time
import typing

import pygame
from entec_pro.controller import Controller

from rtmidi.midiutil import open_midiinput

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)

pixels = typing.Dict[int, typing.Tuple[int, int, int]]

# pygame.init()
# size = [400, 300]
# screen = pygame.display.set_mode(size)

def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class LightBar:
    """A class for working with lightbar at 96 channel mode."""
    def __init__(self, start_address: int):
        self.start_address = start_address
        self.pixels = {}
        for i in range(32):
            self.pixels[i] = (0, 0, 0)

    pixels: typing.Dict[int, typing.Tuple[int, int, int]]

    def set_pixel(self, pixel: int, color: typing.Tuple[int, int, int]):
        self.pixels[pixel] = color

    def clear_pixels(self):
        for pixel in self.pixels:
            self.pixels[pixel] = (0, 0, 0)

    def send_to_controller(self, controller: Controller):
        for pixel, color in self.pixels.items():
            controller.set_channel((self.start_address)+3*pixel, color[0])  # R
            controller.set_channel((self.start_address+1)+3*pixel, color[1])  # G
            controller.set_channel((self.start_address+2)+3*pixel, color[2])  # B

def beat_square_to_lightbar_mapping(beat_square_position: int, lightbars: typing.List[LightBar]) -> typing.List[pixels]:
    """Returns a list of pixels for each lightbar."""
    pixels = []
    for lightbar in lightbars:
        pixels.append(lightbar.pixels[beat_square_position])
    return pixels

Color = typing.Tuple[int, int, int]


class UpdateFrequency(enum.Enum):
    BEAT = 1
    HALF_BEAT = 2
    QUARTER_BEAT = 3
    EVERY_OTHER_BEAT = 4


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

@dataclasses.dataclass
class RandomColorChangesLightBar:
    update_frequency: UpdateFrequency = UpdateFrequency.HALF_BEAT
    lightbar_color: typing.List[Color] = dataclasses.field(default_factory=lambda: [generate_random_color() for i in range(3)])
    bar_update_type: ColorChangeLightBar = OrganizedUpdateOfLightbars()
    counter = 0


class Mode(enum.Enum):
    DRAW_TOWARDS_RIGHT = 1
    RAINBOW_BLINK = 2
    BLINK = 3
    BEAT_SQUARE = 4
    BEAT_SQUARE_BOUNCING = 5
    RANDOM_LIGHTBAR_CHANGES_COLOR = RandomColorChangesLightBar()

class Direction(enum.Enum):
    RIGHT = 1
    LEFT = 2

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()
        self.pulse_counter = 0
        self.beat_number = 0
        self.lightbar = LightBar(1)
        self.lightbar_two = LightBar(97)
        self.lightbar_three = LightBar(193)
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
                        self.lightbar_order[1].set_pixel(lightbar_pixel_mod-32, self.current_color)
                        self.lightbar_order[1].send_to_controller(ctrl)
                    else:
                        self.lightbar_order[2].set_pixel(lightbar_pixel_mod-64, self.current_color)
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
                        bars_to_change = self.mode.value.bar_update_type.lightbar_pairings[self.mode.value.counter%len(self.mode.value.bar_update_type.lightbar_pairings)]
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
                            self.lightbar_order[1].set_pixel(pixel_position-32, self.current_color)
                        else:
                            self.lightbar_order[2].set_pixel(pixel_position-64, self.current_color)

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
                            96-(int((self.pulse_counter * step) + 4)),
                            96-(int((self.pulse_counter * step) + 3)),
                            96-(int((self.pulse_counter * step) + 2)),
                            96-(int((self.pulse_counter * step) + 1)),
                            96-(int((self.pulse_counter * step) + 0)),
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
                            self.lightbar_order[1].set_pixel(pixel_position-32, self.current_color)
                        else:
                            self.lightbar_order[2].set_pixel(pixel_position-64, self.current_color)

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


# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.


# Address 1-96: Lightbar 1
# Address 97-192: Lightbar 2
# Address 193-288: Lightbar 3
# Address 289-296: Left eye dragon left
# Address 297-304: Left eye dragon right
# Address 305-312: Right eye dragon left
# Address 313-320: Right eye dragon right
# Address ??: Smoke machine left
# Address ??: Smoke machine right

ctrl = Controller(
    port_string="/dev/cu.usbserial-EN379589",
    dmx_size=512,
    baudrate=250000,
    timeout=1,
    auto_submit=False,
)





def main():
    port = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        midiin, port_name = open_midiinput(port)
        midiin.ignore_types(sysex=True,
                            timing=False,
                            active_sense=True)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    print("Attaching MIDI input callback handler.")
    midiin.set_callback(MidiInputHandler(port_name))

    print("Entering main loop. Press Control-C to exit.")
    try:
        # Just wait for keyboard interrupt,
        # everything else is handled via the input callback.
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin


# Dragon eye:
# Channel 1: Master dimmer, overrides all RGB dimmers. Would just use 0 for off and 255 for ON, or just leave alwayw on tbh...
# Channel 2: Red dimmer, 0 is off, 255 is max. 255 is blinding. 155 is very bright but not blinding. 30 is ok but not weak.
# Channel 3: Green dimmer, 0 is off, 255 is max. 255 is blinding. 155 is very bright but not blinding. 30 is ok but not weak.
# Channel 4: Blue dimmer, 0 is off, 255 is max. 255 is blinding. 155 is very bright but not blinding. 30 is ok but not weak.
# Channel 5 is skip mode. Very undocumented. Various blinks from 200-255. Not very useful imho and probably easier to program ourselves.
# Channel 6 is strobe speed. 255 is seisure fast. 100 is airstrip kind of blink. 10 is kinda similar to 100.
# Channel 7 seems useless. A combo of the skip and strobe above, and also has a "fade mode" that only seems like preprogrammed fades.
# Trenger minst 0.2 sek mellom man raiser lys, og man tar de ned igjen, om ikke blir det støgt.

# Smoke machine:
# Channel 1: Smoke emission
# Channel 2: Red ligjt
# Channel 3: Green light
# Channel 4: Blue light
# Channel 5: LED flash
# Channel 6: 30-179 is color fade, 180-255 is color skip
# Channel 7: Speed adjust (ooooh!) - seems kinda BS. 1 is just forever slow, and any value over 50 is near instant.

# Colors do mix! But not evenly.
# Smoke on is quite precise, but smoke off isnt
# Compared to the eyes, here you can actually smoothly while loop all the way up and down without any sleep.
# ... seems like the LED par cans are kinda shit:D
# (Should have known given the price...)

if __name__ == "__main__":
    # main()

    # SMOKE
    #ctrl.set_channel(2,209)
    #ctrl.set_channel(1,255)
    #time.sleep(2)
    #ctrl.set_channel(1,0)


    # RED LIGHT

    # GREEN LIGHT
    #ctrl.set_channel(3,109)

    # BLUE LIGHT
    while True:
        for i in range(255):
            ctrl.set_channel(4,i)
            ctrl.submit()

        for i in reversed(range(255)):
            ctrl.set_channel(4,i)
            ctrl.submit()

    # LED FLASH
    # ctrl.set_channel(5,255)

    # COLOR FADE
    # ctrl.set_channel(6,255)

    # SPEED ADJUST
    ctrl.set_channel(7,255)

    ctrl.submit()

