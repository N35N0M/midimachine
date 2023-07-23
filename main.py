from __future__ import print_function

import sys
import time
import pygame
from rtmidi.midiutil import open_midiinput

from lightbar.lightbar_designer import LightbarDesigner
from midi.midi_input_handler import MidiInputHandler
from stage.pygame_adapter import map_stage_to_pygame
from stage.stage import create_stage
from utils import generate_random_color

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
    midi_input_handler = MidiInputHandler(port_name)
    midiin.set_callback(midi_input_handler)

    print("Initializing stage")
    pygame.init()
    surface = pygame.display.set_mode((1190, 300))


    stage = create_stage()
    lightbar_designer = LightbarDesigner(midi_input_handler, stage.lightbar_one, stage.lightbar_three, stage.lightbar_two)

    print("Entering main loop. Press Control-C to exit.")
    try:
        while True:
            # Refresh at 44Hz (the "standard" framerate for DMX)
            map_stage_to_pygame(stage, surface)
            # map_stage_to_dmx(stage)
            stage.dragon_left.left_eye = generate_random_color()
            time.sleep(1 / 44)

    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin




if __name__ == "__main__":
    main()

