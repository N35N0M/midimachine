from __future__ import print_function

import pygame

from dragon.dragon import Dragon
from lightbar.lightbar import LightBar
from stage.stage import Stage_2023


def lightbar_to_pygame(lightbar: LightBar, x_pos: int, y_pos: int, surface) -> None:
    """
    Draws the lightbar in the pygame window at the specified position.
    """

    pixel_size = 10
    for i in range(len(lightbar.pixels)):
        final_position = x_pos + i * pixel_size
        if i != 0:
            # Pad between pixels
            final_position += 2 * i
        pygame.draw.rect(
            surface=surface,
            color=(lightbar.pixels[i].red, lightbar.pixels[i].green, lightbar.pixels[i].blue),
            rect=pygame.Rect(final_position, y_pos, pixel_size, pixel_size
                             )
        )
    pygame.draw.line(
        surface=surface,
        color=(255, 255, 255),
        start_pos=(x_pos, y_pos + 12),
        end_pos=(x_pos + 31 * pixel_size + 2 * 31 + pixel_size, y_pos + 12)
    )
    font = pygame.font.SysFont(None, 24)
    img = font.render(lightbar.label, True, (255, 255, 255))
    surface.blit(img, (x_pos + 135, y_pos + 13))


def dragon_to_pygame(dragon: Dragon, x_pos: int, y_pos: int, surface) -> None:
    """
    Draws the dragon in the pygame window at the specified position.
    """
    dragon_icon = pygame.image.load('dragon_icon.png')
    dragon_icon = pygame.transform.scale(dragon_icon, (100, 100))

    dragon_breath = pygame.image.load('fire.jpg')
    dragon_breath = pygame.transform.scale(dragon_breath, (50, 50))
    dragon_breath = pygame.transform.rotate(dragon_breath, 180)
    surface.blit(dragon_icon, (x_pos, y_pos))

    if dragon.smoke_machine_on:
        surface.blit(dragon_breath, (x_pos+25, y_pos+100))

    pygame.draw.rect(
        surface=surface,
        color=(dragon.left_eye.red, 0, 0),
        rect=pygame.Rect(x_pos+5, y_pos+50, 20, 20
                         )
    )
    pygame.draw.rect(
        surface=surface,
        color=(0, dragon.left_eye.green, 0),
        rect=pygame.Rect(x_pos+25, y_pos+50, 20, 20
                            )
    )
    pygame.draw.rect(
        surface=surface,
        color=(0, 0, dragon.left_eye.blue),
        rect=pygame.Rect(x_pos+15, y_pos+30, 20, 20
                            )
    )


    pygame.draw.rect(
        surface=surface,
        color=(dragon.right_eye.red, 0, 0),
        rect=pygame.Rect(x_pos+55, y_pos+50, 20, 20
                         )
    )
    pygame.draw.rect(
        surface=surface,
        color=(0, dragon.right_eye.green, 0),
        rect=pygame.Rect(x_pos+75, y_pos+50, 20, 20
                         )
    )
    pygame.draw.rect(
        surface=surface,
        color=(0, 0, dragon.right_eye.blue),
        rect=pygame.Rect(x_pos+65, y_pos+30, 20, 20
                         )
    )


def map_stage_to_pygame(stage: Stage_2023, surface) -> None:
    surface.fill((0, 0, 0))
    lightbar_to_pygame(
        lightbar=stage.lightbar_one,
        x_pos=5,
        y_pos=200,
        surface=surface
    )

    lightbar_to_pygame(
        lightbar=stage.lightbar_two,
        x_pos=405,
        y_pos=200,
        surface=surface
    )

    lightbar_to_pygame(
        lightbar=stage.lightbar_three,
        x_pos=805,
        y_pos=200,
        surface=surface
    )

    dragon_to_pygame(stage.dragon_left, 350, 5, surface)
    dragon_to_pygame(stage.dragon_right, 750, 5, surface)

    font = pygame.font.SysFont("arial", 24)
    img = font.render(f"Deck A: {stage.traktor_metadata.current_track_deck_a}", True, (255, 255, 255))
    surface.blit(img, (50, 250))

    font = pygame.font.SysFont("arial", 24)
    img = font.render(f"{stage.traktor_metadata.current_track_elapsed_deck_a}", True, (255, 255, 255))
    surface.blit(img, (550, 250))

    pygame.display.flip()