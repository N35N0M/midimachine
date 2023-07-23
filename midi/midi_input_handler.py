from __future__ import print_function

import logging
import time

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()
        self.pulse_counter = 0
        self.beat_number = 0
        self.estimated_bpm = 0

    def set_mode(self, mode):
        self.mode = mode

    def __call__(self, event, data=None):
        message, deltatime = event
        if message == [248]:
            self.pulse_counter += 1
            if deltatime == 0:
                return
            pulses_per_quarter_note = 24
            self.estimated_bpm = 60 * (1000 / deltatime) / pulses_per_quarter_note
        elif message == [250]:
            print("MIDI clock enabled!")
            self.pulse_counter = 0
            self.pulse_effect_started = False
        elif message == [252]:
            print("MIDI clock disabled!")
            self.pulse_counter = 0
        else:
            print(message)