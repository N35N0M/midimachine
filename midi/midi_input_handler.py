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
        self.on_beat_callbacks = []
        self.on_pulse_callbacks = []

    def set_mode(self, mode):
        self.mode = mode

    def notify_on_beat(self, callback):
        self.on_beat_callbacks.append(callback)

    def notify_on_pulse(self, callback):
        self.on_pulse_callbacks.append(callback)

    def __call__(self, event, data=None):
        message, deltatime = event
        if message == [248]:
            self.pulse_counter += 1
            for callback in self.on_pulse_callbacks:
                callback()
            if deltatime == 0:
                return
            pulses_per_quarter_note = 24
            self.estimated_bpm = 60 * (1000 / deltatime) / pulses_per_quarter_note

            if self.pulse_counter % 24 == 0:
                self.beat_number += 1
                for callback in self.on_beat_callbacks:
                    callback()
                print("Beat number: {}".format(self.beat_number))
                print("Estimated BPM: {}".format(self.estimated_bpm))
                print("Pulse counter: {}".format(self.pulse_counter))
                print("Delta time: {}".format(deltatime))
        elif message == [250]:
            print("MIDI clock enabled!")
            self.pulse_counter = 0
            self.pulse_effect_started = False
        elif message == [252]:
            print("MIDI clock disabled!")
            self.pulse_counter = 0
        else:
            print(message)