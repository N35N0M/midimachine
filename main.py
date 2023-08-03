from __future__ import print_function

import json
import os
import threading
import time
import pygame
from rtmidi.midiutil import open_midiinput
import DMXEnttecPro.src.DMXEnttecPro.controller as dmx_driver
from dragon.dragon_designer import DragonDesigner
from lightbar.lightbar_designer import LightbarDesigner
from midi.midi_input_handler import MidiInputHandler
from stage.dmx_adapter import map_stage_to_dmx
from stage.pygame_adapter import map_stage_to_pygame
from stage.stage import create_stage
from traktor_metadata import TraktorMetadata

import sys

from flask import Flask, request, jsonify
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)

traktor_metadata = TraktorMetadata()

simulation = os.getenv("SIMULATION", None)

@app.route('/deckLoaded/<deck>', methods=['POST', 'GET'])
def deckLoaded(deck):
   if request.method == 'POST':
      if deck == "1":
         traktor_metadata.current_track_deck_a = json.loads(request.data)["value"]
         traktor_metadata.current_track_elapsed_deck_a = json.loads(request.data)["elapsed"]
      elif deck == "2":
            traktor_metadata.current_track_deck_b = json.loads(request.data)["value"]
            traktor_metadata.current_track_elapsed_deck_b = json.loads(request.data)["elapsed"]
      return jsonify(success=True)
   else:
      return jsonify(success=True)

@app.route('/updateMasterClock', methods=['POST', 'GET'])
def updateMasterClock():
    if request.method == 'POST':
        traktor_metadata.master_deck = json.loads(request.data)["deck"]
        print(json.loads(request.data))
        return jsonify(success=True)
    else:
        return jsonify(success=True)

if simulation is None:
    ctrl = dmx_driver.Controller(
        port_string="/dev/cu.usbserial-EN379589",
        dmx_size=512,
        baudrate=250000,
        timeout=1,
        auto_submit=False,
    )
else:
    ctrl = None

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

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

    stage = create_stage(traktor_metadata)
    lightbar_designer = LightbarDesigner(midi_input_handler, stage.lightbar_one, stage.lightbar_three, stage.lightbar_two, traktor_metadata)
    dragon_designer = DragonDesigner(midi_input_handler, stage)
    print("Entering main loop. Press Control-C to exit.")
    try:
        while True:
            # Refresh at 44Hz (the "standard" framerate for DMX)
            map_stage_to_pygame(stage, surface)

            if ctrl is not None:
                map_stage_to_dmx(stage, ctrl)
            time.sleep(1 / 44)

    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin



# Channel 1-96 (96ch, 3ch per pixel): Lightbar left
# Channel 97-192 (96ch, 3ch per pixel): Lightbar Center
# Channel 193-288 (96ch, 3ch per pixel): Lightbar Right
# Channel 289-295 (7ch, ch 1 = master dimmer?, ch2,3,4 = RGB?): Dragon left eye left
# Channel 296-302(7ch): Dragon left eye right
# Channel 303-308 (6ch, ch1 smoke emit, ch2 hardcode 0 for color select, ch3-5 is RGB): Dragon left smoke
# Channel 309-315(7ch): Dragon right eye left
# Channel 316-322 (7ch): Dragon right eye right
# Channel 323-328 (6ch, ch1 smoke emit, ch2 hardcode 0 for color select, ch3-5 is RGB): Dragon right smoke
if __name__ == "__main__":
    print("Clearing channels!")
    for i in range(1, 513):
        ctrl.set_channel(i, 0)
    ctrl.submit()

    print("Testing left sidebar!")
    ctrl.set_channel(1, 255)
    ctrl.submit()
    time.sleep(1)

    print("Testing center sidebar!")
    ctrl.set_channel(97, 255)
    ctrl.submit()
    time.sleep(1)

    print("Testing right sidebar!")
    ctrl.set_channel(193, 255)
    ctrl.submit()
    time.sleep(1)

    print("Testing left-dragon left-eye")
    ctrl.set_channel(289, 255)
    ctrl.set_channel(291, 255)
    ctrl.submit()
    time.sleep(1)

    print("Testing left-dragon right-eye")
    ctrl.set_channel(296, 255)
    ctrl.set_channel(298, 255)
    ctrl.submit()
    time.sleep(1)

    print("Testing left-dragon smoke")
    ctrl.set_channel(303, 255)
    ctrl.set_channel(304, 0)
    ctrl.set_channel(305, 255)
    ctrl.submit()
    time.sleep(1)
    ctrl.set_channel(303, 0)
    ctrl.submit()
    time.sleep(1)

    print("Testing right-dragon left-eye")
    ctrl.set_channel(309, 255)
    ctrl.set_channel(311, 255)
    ctrl.submit()
    time.sleep(1)

    print("Testing right-dragon right-eye")
    ctrl.set_channel(316, 255)
    ctrl.set_channel(318, 255)
    ctrl.submit()
    time.sleep(1)

    print("Testing right-dragon smoke")
    ctrl.set_channel(323, 255)
    ctrl.set_channel(324, 0)
    ctrl.set_channel(325, 255)
    ctrl.submit()
    time.sleep(1)
    ctrl.set_channel(323, 0)
    ctrl.submit()
    time.sleep(1)



    threading.Thread(target=lambda: app.run(debug=False, use_reloader=False)).start()
    main()

