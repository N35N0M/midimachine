from __future__ import print_function

import DMXEnttecPro.src.DMXEnttecPro.controller as dmx_driver
from stage.stage import Stage_2023


# Channel 1-96 (96ch, 3ch per pixel): Lightbar left
# Channel 97-192 (96ch, 3ch per pixel): Lightbar Center
# Channel 193-288 (96ch, 3ch per pixel): Lightbar Right
# Channel 289-295 (7ch, ch 1 = master dimmer?, ch2,3,4 = RGB?): Dragon left eye left
# Channel 296-302(7ch): Dragon left eye right
# Channel 303-308 (6ch, ch1 smoke emit, ch2 hardcode 0 for color select, ch3-5 is RGB): Dragon left smoke
# Channel 309-315(7ch): Dragon right eye left
# Channel 316-322 (7ch): Dragon right eye right
# Channel 323-328 (6ch, ch1 smoke emit, ch2 hardcode 0 for color select, ch3-5 is RGB): Dragon right smoke


def map_stage_to_dmx(stage: Stage_2023, dmx_controller: dmx_driver) -> None:

    # Map left lightbar
    current_channel = 1
    for pixel in stage.lightbar_one.pixels:
        dmx_controller.set_channel(current_channel, pixel.red)
        dmx_controller.set_channel(current_channel+1, pixel.green)
        dmx_controller.set_channel(current_channel+2, pixel.blue)
        current_channel += 3

    assert current_channel == 97

    # Map center lightbar
    for pixel in stage.lightbar_two.pixels:
        dmx_controller.set_channel(current_channel, pixel.red)
        dmx_controller.set_channel(current_channel+1, pixel.green)
        dmx_controller.set_channel(current_channel+2, pixel.blue)
        current_channel += 3

    assert current_channel == 193

    # Map right lightbar
    for pixel in stage.lightbar_three.pixels:
        dmx_controller.set_channel(current_channel, pixel.red)
        dmx_controller.set_channel(current_channel+1, pixel.green)
        dmx_controller.set_channel(current_channel+2, pixel.blue)
        current_channel += 3

    assert current_channel == 289

    # Map left-dragon left-eye
    dmx_controller.set_channel(current_channel, 255)  # Master dimmer?
    dmx_controller.set_channel(current_channel+1, stage.dragon_left.left_eye.red)  # Red?
    dmx_controller.set_channel(current_channel+2, stage.dragon_left.left_eye.green)  # Green?
    dmx_controller.set_channel(current_channel+3, stage.dragon_left.left_eye.blue)  # Blue?
    current_channel += 7

    assert current_channel == 296

    # Map left-dragon right-eye
    dmx_controller.set_channel(current_channel, 255)  # Master dimmer?
    dmx_controller.set_channel(current_channel+1, stage.dragon_left.right_eye.red)  # Red?
    dmx_controller.set_channel(current_channel+2, stage.dragon_left.right_eye.green)  # Green?
    dmx_controller.set_channel(current_channel+3, stage.dragon_left.right_eye.blue)  # Blue?

    current_channel += 7

    assert current_channel == 303

    # Map left-dragon smoke
    dmx_controller.set_channel(current_channel, 255 if stage.dragon_left.smoke_machine_on else 0)  # Smoke emit
    dmx_controller.set_channel(current_channel+1, 0)  # Hardcode 0 for color select
    dmx_controller.set_channel(current_channel+3, 255 if stage.dragon_left.smoke_machine_on else 0)  # Green

    current_channel += 6

    assert current_channel == 309

    # Map right-dragon left-eye
    dmx_controller.set_channel(current_channel, 255)  # Master dimmer?
    dmx_controller.set_channel(current_channel+1, stage.dragon_right.left_eye.red)  # Red?
    dmx_controller.set_channel(current_channel+2, stage.dragon_right.left_eye.green)  # Green?
    dmx_controller.set_channel(current_channel+3, stage.dragon_right.left_eye.blue)  # Blue?

    current_channel += 7

    assert current_channel == 316

    # Map right-dragon right-eye
    dmx_controller.set_channel(current_channel, 255)  # Master dimmer?
    dmx_controller.set_channel(current_channel+1, stage.dragon_right.right_eye.red)  # Red?
    dmx_controller.set_channel(current_channel+2, stage.dragon_right.right_eye.green)  # Green?
    dmx_controller.set_channel(current_channel+3, stage.dragon_right.right_eye.blue)  # Blue?

    current_channel += 7

    assert current_channel == 323

    # Map right-dragon smoke
    dmx_controller.set_channel(current_channel, 255 if stage.dragon_right.smoke_machine_on else 0)  # Smoke emit
    dmx_controller.set_channel(current_channel+1, 0)  # Hardcode 0 for color select
    dmx_controller.set_channel(current_channel+3, 255 if stage.dragon_right.smoke_machine_on else 0)  # Green

    current_channel += 6

    assert current_channel == 329

    dmx_controller.submit()