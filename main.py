from __future__ import print_function

import json
import threading
import time
import pygame
from rtmidi.midiutil import open_midiinput

from dragon.dragon_designer import DragonDesigner
from lightbar.lightbar_designer import LightbarDesigner
from midi.midi_input_handler import MidiInputHandler
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
            # map_stage_to_dmx(stage)
            time.sleep(1 / 44)

    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin




if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(debug=False, use_reloader=False)).start()
    main()

