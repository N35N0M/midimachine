import threading
import time
import typing
from enum import Enum

from common_types import RgbPixel
from dragon.dragon import Dragon
from lightbar.lightbar_designer import UpdateType
from midi.midi_input_handler import MidiInputHandler
from stage.stage import Stage_2023

class LastFired(Enum):
    LEFT = 1
    RIGHT = 2

class ThomasState:
    last_fired: LastFired = LastFired.RIGHT

class DragonMode(Enum):
    THOMAS_THE_TANK_ENGINE = 1
    EYES_OFF = 2
    ALL_OFF = 3
    PULSING_EYES = 4
    CRAZY_EYES = 5

class DragonDesigner:
    def __init__(self, midi_clock, stage: Stage_2023):
        self.midi_clock: MidiInputHandler = midi_clock
        self.stage = stage
        self.mode = DragonMode.THOMAS_THE_TANK_ENGINE
        self.modestate:  typing.Union[ThomasState, None] = None
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

    def dragon_fire(self, dragon: Dragon):
        def dragon_burst(dragon):
            dragon.smoke_machine_on = True
            time.sleep(1)
            dragon.smoke_machine_on = False
        thr = threading.Thread(target=dragon_burst, args=(dragon,), kwargs={})
        thr.start()

    def render(self, update_type):
        current_track = self.stage.traktor_metadata.current_track_deck_a if self.stage.traktor_metadata.master_deck == 'A' else self.stage.traktor_metadata.current_track_deck_b
        current_track_elapsed = self.stage.traktor_metadata.current_track_elapsed_deck_a if self.stage.traktor_metadata.master_deck == 'A' else self.stage.traktor_metadata.current_track_elapsed_deck_b
        if current_track == "Biggie smalls the tank engine":
            self.mode = DragonMode.THOMAS_THE_TANK_ENGINE
            if self.modestate is None:
                self.modestate = ThomasState()
        elif current_track == "Amberina Sun":
            if 249.5 > current_track_elapsed > 209:
                self.mode = DragonMode.PULSING_EYES
            else:
                self.mode = DragonMode.ALL_OFF

            if 230 < current_track_elapsed < 234:
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "The Girl and the Robot":
            # Eye cues
            if (16 < current_track_elapsed < 31) or \
                    (80 < current_track_elapsed < 95) or \
                    (144 < current_track_elapsed < 158) or \
                    (159 < current_track_elapsed < 173):
                self.mode = DragonMode.PULSING_EYES
            elif (48 < current_track_elapsed < 78) or \
                    (111 < current_track_elapsed < 126) or \
                    (134 < current_track_elapsed < 159) or \
                    (198 < current_track_elapsed < 236) or \
                    (0 < current_track_elapsed < 16):
                self.mode = DragonMode.CRAZY_EYES
            else:
                self.mode = DragonMode.EYES_OFF

            # Smoke cues
            if (21 < current_track_elapsed < 31) or \
                    (127 < current_track_elapsed < 134):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        else:
            self.mode = DragonMode.PULSING_EYES

        if self.mode == DragonMode.ALL_OFF:
            self.stage.dragon_left.left_eye = RgbPixel(0, 0, 0)
            self.stage.dragon_left.right_eye = RgbPixel(0, 0, 0)
            self.stage.dragon_right.left_eye = RgbPixel(0, 0, 0)
            self.stage.dragon_right.right_eye = RgbPixel(0, 0, 0)
            self.stage.dragon_left.smoke_machine_on = False
            self.stage.dragon_right.smoke_machine_on = False
            return
        if self.mode == DragonMode.EYES_OFF:
            self.stage.dragon_left.left_eye = RgbPixel(0, 0, 0)
            self.stage.dragon_left.right_eye = RgbPixel(0, 0, 0)
            self.stage.dragon_right.left_eye = RgbPixel(0, 0, 0)
            self.stage.dragon_right.right_eye = RgbPixel(0, 0, 0)
            return
        if self.mode == DragonMode.PULSING_EYES:
            counter_val = self.internal_pulse_counter % 48
            if counter_val < 24:
                self.stage.dragon_left.left_eye = RgbPixel(0, 0, int((255/24)*counter_val))
                self.stage.dragon_left.right_eye = RgbPixel(0, 0, int((255/24)*counter_val))
                self.stage.dragon_right.left_eye = RgbPixel(0, 0, int((255/24)*counter_val))
                self.stage.dragon_right.right_eye = RgbPixel(0, 0, int((255/24)*counter_val))
            else:
                self.stage.dragon_left.left_eye = RgbPixel(0, 0, int(255 - ((255/24)*(counter_val-24))))
                self.stage.dragon_left.right_eye = RgbPixel(0, 0, int(255 - ((255/24)*(counter_val-24))))
                self.stage.dragon_right.left_eye = RgbPixel(0, 0, int(255 - ((255/24)*(counter_val-24))))
                self.stage.dragon_right.right_eye = RgbPixel(0, 0, int(255 - ((255/24)*(counter_val-24))))

        if self.mode == DragonMode.CRAZY_EYES:
            counter_val = self.internal_pulse_counter % (96)
            if 0 < counter_val < 24:
                self.stage.dragon_left.left_eye = RgbPixel(0, 0, int((255/24)*counter_val))
                self.stage.dragon_left.right_eye = RgbPixel(0, 0, int((255/24)*counter_val))
                self.stage.dragon_right.left_eye = RgbPixel(0, 0, int((255/24)*counter_val))
                self.stage.dragon_right.right_eye = RgbPixel(0, 0, int((255/24)*counter_val))
            if 24 < counter_val < 48:
                self.stage.dragon_left.left_eye = RgbPixel(0, 0, int(255 - ((255/24)*(counter_val-24))))
                self.stage.dragon_left.right_eye = RgbPixel(0, 0, int(255 - ((255/24)*(counter_val-24))))
                self.stage.dragon_right.left_eye = RgbPixel(0, 0, int(255 - ((255/24)*(counter_val-24))))
                self.stage.dragon_right.right_eye = RgbPixel(0, 0, int(255 - ((255/24)*(counter_val-24))))

                self.stage.dragon_left.left_eye = RgbPixel(0, int((255 / 24) * (counter_val-24)), 0)
                self.stage.dragon_left.right_eye = RgbPixel(0, int((255 / 24) * (counter_val-24)), 0)
                self.stage.dragon_right.left_eye = RgbPixel(0, int((255 / 24) * (counter_val-24)), 0)
                self.stage.dragon_right.right_eye = RgbPixel(0, int((255 / 24) * (counter_val-24)), 0)
            if 48 < counter_val < 72:
                self.stage.dragon_left.left_eye = RgbPixel(0, int(255 - ((255 / 24) * (counter_val - 48))), 0)
                self.stage.dragon_left.right_eye = RgbPixel(0, int(255 - ((255 / 24) * (counter_val - 48))), 0)
                self.stage.dragon_right.left_eye = RgbPixel(0, int(255 - ((255 / 24) * (counter_val - 48))), 0)
                self.stage.dragon_right.right_eye = RgbPixel(0, int(255 - ((255 / 24) * (counter_val - 48))), 0)

                self.stage.dragon_left.left_eye = RgbPixel(int((255 / 24) * (counter_val-48)), 0, 0)
                self.stage.dragon_left.right_eye = RgbPixel(int((255 / 24) * (counter_val-48)), 0, 0)
                self.stage.dragon_right.left_eye = RgbPixel(int((255 / 24) * (counter_val-48)), 0, 0)
                self.stage.dragon_right.right_eye = RgbPixel(int((255 / 24) * (counter_val-48)), 0, 0)
            if counter_val > 72:
                self.stage.dragon_left.left_eye = RgbPixel(int(255 - ((255 / 24) * (counter_val - 72))), 0, 0)
                self.stage.dragon_left.right_eye = RgbPixel(int(255 - ((255 / 24) * (counter_val - 72))), 0, 0)
                self.stage.dragon_right.left_eye = RgbPixel(int(255 - ((255 / 24) * (counter_val - 72))), 0, 0)
                self.stage.dragon_right.right_eye = RgbPixel(int(255 - ((255 / 24) * (counter_val - 72))), 0, 0)


        if update_type == UpdateType.BEAT:
            if self.mode == DragonMode.THOMAS_THE_TANK_ENGINE:
                counter_val = self.internal_pulse_counter % 48
                if counter_val < 24:
                    self.stage.dragon_left.left_eye = RgbPixel(0, 0, int((255 / 24) * counter_val))
                    self.stage.dragon_left.right_eye = RgbPixel(0, 0, int((255 / 24) * counter_val))
                    self.stage.dragon_right.left_eye = RgbPixel(0, 0, int((255 / 24) * counter_val))
                    self.stage.dragon_right.right_eye = RgbPixel(0, 0, int((255 / 24) * counter_val))
                else:
                    self.stage.dragon_left.left_eye = RgbPixel(0, 0, int(255 - ((255 / 24) * (counter_val - 24))))
                    self.stage.dragon_left.right_eye = RgbPixel(0, 0, int(255 - ((255 / 24) * (counter_val - 24))))
                    self.stage.dragon_right.left_eye = RgbPixel(0, 0, int(255 - ((255 / 24) * (counter_val - 24))))
                    self.stage.dragon_right.right_eye = RgbPixel(0, 0, int(255 - ((255 / 24) * (counter_val - 24))))

            # See if Thomas is currently under the left or right dragon
            if self.stage.lightbar_one.pixels[31] == RgbPixel(107, 107, 107):
                if self.modestate.last_fired == LastFired.RIGHT:
                    self.dragon_fire(self.stage.dragon_left)
                    self.modestate.last_fired = LastFired.LEFT
            elif self.stage.lightbar_two.pixels[31] == RgbPixel(107, 107, 107):
                if self.modestate.last_fired == LastFired.LEFT:
                    self.dragon_fire(self.stage.dragon_right)
                    self.modestate.last_fired = LastFired.RIGHT