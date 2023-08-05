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
        elif current_track == "Make Me Thomas (feat. Jawn Legend)":
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
        elif current_track == "Junkyard Dunebuggy":
            self.mode = DragonMode.PULSING_EYES
            if (172.3 < current_track_elapsed < 173.3) or \
                    (182.6 < current_track_elapsed < 186) or \
                    (192.1 < current_track_elapsed < 195) or \
                    (96.1 < current_track_elapsed < 97.1) or \
                    (220.3 < current_track_elapsed < 221.6):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False

        elif current_track == "We Don't Need Another Hero (Thunderdome)":
            self.mode = DragonMode.PULSING_EYES
            if (14.8 < current_track_elapsed < 16.8) or (17.3 < current_track_elapsed< 19.3) or \
                    (34 < current_track_elapsed < 36) or (36.5 < current_track_elapsed < 38.5) or \
                    (107 < current_track_elapsed < 109) or (109.5 < current_track_elapsed < 111.5) or \
                    (126.5 < current_track_elapsed < 128.5) or (129 < current_track_elapsed < 131) or \
                    (201 < current_track_elapsed < 205) or \
                    (53.5 < current_track_elapsed < 55.5) or (56.0 < current_track_elapsed < 58.0):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Hot":
            self.mode = DragonMode.PULSING_EYES
            if (66.6 < current_track_elapsed < 70) or (175.2 < current_track_elapsed < 178):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "You Can Do It":
            self.mode = DragonMode.PULSING_EYES
            if (194.5 < current_track_elapsed < 209.9):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "The Final Countdown":
            self.mode = DragonMode.PULSING_EYES
            if (53.86 < current_track_elapsed < 78.0):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (119 < current_track_elapsed < 123.0):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (168 < current_track_elapsed < 174.0):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (253 < current_track_elapsed < 255.0):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Santa Catarina":
            self.mode = DragonMode.PULSING_EYES
            if (217 < current_track_elapsed < 233):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Cha Cha Cha":
            if (34.2 < current_track_elapsed < 37):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (40.3 < current_track_elapsed < 43.1):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (46.1 < current_track_elapsed < 49.4):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (83.7 < current_track_elapsed < 86.5):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (89.9 < current_track_elapsed < 92.7):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (89.9 < current_track_elapsed < 92.7):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (96.1 < current_track_elapsed < 98.8):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (161.1 < current_track_elapsed < 164):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (167.3 < current_track_elapsed < 170):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.mode = DragonMode.PULSING_EYES
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Tor Kraft":
            self.mode = DragonMode.PULSING_EYES
            if (42.96 < current_track_elapsed < 46.6):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (90.8 < current_track_elapsed < 95):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (104.2 < current_track_elapsed < 107.2):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (120.8 < current_track_elapsed < 126.6):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Time Machine":
            self.mode = DragonMode.PULSING_EYES
            if (54.8 < current_track_elapsed < 59):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (133.5 < current_track_elapsed < 140):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (178.5 < current_track_elapsed < 188):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Gentleman":
            self.mode = DragonMode.PULSING_EYES
            if (8.1 < current_track_elapsed < 15.7):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (61.4 < current_track_elapsed < 70):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (124 < current_track_elapsed < 134):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (162.4 < current_track_elapsed < 172):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Hogwarts' March - Flawless Remix":
            if (52 < current_track_elapsed < 54):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (67 < current_track_elapsed < 69):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (112.7 < current_track_elapsed < 115):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.mode = DragonMode.PULSING_EYES
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Skibidi (Romantic Edition)":
            self.mode = DragonMode.PULSING_EYES
            if (7.9 < current_track_elapsed < 14.5):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "City Boy":
            self.mode = DragonMode.PULSING_EYES
            if (134 < current_track_elapsed < 144):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "10 Years (Chromeo Remix)":
            self.mode = DragonMode.PULSING_EYES
            if (135.7 < current_track_elapsed < 143):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Bitter Kitten":
            if (69.1 < current_track_elapsed < 79):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.mode = DragonMode.PULSING_EYES
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Disco Guy (Original Version)":
            self.mode = DragonMode.PULSING_EYES
            if (193 < current_track_elapsed < 213):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Jeg Vil Bare Danse":
            self.mode = DragonMode.PULSING_EYES
            if (52.4 < current_track_elapsed < 55):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (134.7 < current_track_elapsed < 137):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Crescendolls":
            self.mode = DragonMode.PULSING_EYES
            if (145< current_track_elapsed < 148):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Keep Moving":
            self.mode = DragonMode.PULSING_EYES
            if (115.0 < current_track_elapsed < 117):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (121.0 < current_track_elapsed < 123):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (125.6 < current_track_elapsed < 128):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (130 < current_track_elapsed < 132):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            elif (149.3 < current_track_elapsed < 151):
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.mode = DragonMode.PULSING_EYES
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        elif current_track == "Bezos I":
            self.mode = DragonMode.PULSING_EYES
            if (41.5 < current_track_elapsed < 56):
                self.mode = DragonMode.CRAZY_EYES
                self.stage.dragon_left.smoke_machine_on = True
                self.stage.dragon_right.smoke_machine_on = True
            else:
                self.mode = DragonMode.PULSING_EYES
                self.stage.dragon_left.smoke_machine_on = False
                self.stage.dragon_right.smoke_machine_on = False
        else:
            self.mode = DragonMode.PULSING_EYES
            self.stage.dragon_left.smoke_machine_on = False
            self.stage.dragon_right.smoke_machine_on = False


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
            if update_type == UpdateType.BEAT:
                if self.internal_beat_counter % 2 == 0:
                    self.internal_pulse_counter = 0
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
            if update_type == UpdateType.BEAT:
                if self.internal_beat_counter % 3 == 0:
                    self.stage.dragon_left.left_eye = RgbPixel(255, 0, 0)
                    self.stage.dragon_left.right_eye = RgbPixel(255, 0, 0)
                    self.stage.dragon_right.left_eye = RgbPixel(255, 0, 0)
                    self.stage.dragon_right.right_eye = RgbPixel(255, 0, 0)
                elif self.internal_beat_counter % 3 == 1:
                    self.stage.dragon_left.left_eye = RgbPixel(0, 255, 0)
                    self.stage.dragon_left.right_eye = RgbPixel(0, 255, 0)
                    self.stage.dragon_right.left_eye = RgbPixel(0, 255, 0)
                    self.stage.dragon_right.right_eye = RgbPixel(0, 255, 0)
                elif self.internal_beat_counter % 3 == 2:
                    self.stage.dragon_left.left_eye = RgbPixel(0, 0, 255)
                    self.stage.dragon_left.right_eye = RgbPixel(0, 0, 255)
                    self.stage.dragon_right.left_eye = RgbPixel(0, 0, 255)
                    self.stage.dragon_right.right_eye = RgbPixel(0, 0, 255)




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
                if self.stage.lightbar_one.pixels[16] == RgbPixel(107, 107, 107):
                    if self.modestate.last_fired == LastFired.RIGHT:
                        self.dragon_fire(self.stage.dragon_left)
                        self.modestate.last_fired = LastFired.LEFT
                elif self.stage.lightbar_three.pixels[16] == RgbPixel(107, 107, 107):
                    if self.modestate.last_fired == LastFired.LEFT:
                        self.dragon_fire(self.stage.dragon_right)
                        self.modestate.last_fired = LastFired.RIGHT