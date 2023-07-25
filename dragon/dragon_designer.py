import threading
import time
import typing
from enum import Enum

from common_types import RgbPixel
from dragon.dragon import Dragon
from lightbar.lightbar import LightBar
from lightbar.lightbar_designer import UpdateType
from midi.midi_input_handler import MidiInputHandler
from stage.stage import Stage_2023
from traktor_metadata import TraktorMetadata

class LastFired(Enum):
    LEFT = 1
    RIGHT = 2

class ThomasState:
    last_fired: LastFired = LastFired.RIGHT

class DragonMode(Enum):
    THOMAS_THE_TANK_ENGINE = 1

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
        thr.start()  # Will run "foo"

    def render(self, update_type):
        if self.stage.traktor_metadata.current_track_deck_a == "Biggie smalls the tank engine":
            self.mode = DragonMode.THOMAS_THE_TANK_ENGINE
            if self.modestate is None:
                self.modestate = ThomasState()
        if update_type == UpdateType.BEAT:
            if self.mode == DragonMode.THOMAS_THE_TANK_ENGINE:
                self.stage.dragon_left.left_eye = RgbPixel(255, 0, 0)
                self.stage.dragon_left.right_eye = RgbPixel(255, 0, 0)

            # See if Thomas is currently under the left or right dragon
            if self.stage.lightbar_one.pixels[31] == RgbPixel(107, 107, 107):
                if self.modestate.last_fired == LastFired.RIGHT:
                    self.dragon_fire(self.stage.dragon_left)
                    self.modestate.last_fired = LastFired.LEFT
            elif self.stage.lightbar_two.pixels[31] == RgbPixel(107, 107, 107):
                if self.modestate.last_fired == LastFired.LEFT:
                    self.dragon_fire(self.stage.dragon_right)
                    self.modestate.last_fired = LastFired.RIGHT