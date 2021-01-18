import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from star import Star
from game_stats import GameStats
from button import Button
import asyncio
from scoreboard import Scoreboard


class Parameters:
    pass


def create_stars(ai_settings, screen):
    return [Star(ai_settings, screen) for _ in range(ai_settings.star_count)]


# мое
async def caption_loop(ai_settings):

    while True:
        for i in range(len(ai_settings.caption)):
            pygame.display.set_caption(ai_settings.caption[i + 1:] + ' ' + ai_settings.caption[0:i+1])
            await asyncio.sleep(0.02)


async def main_loop(PARAM):
    while True:
        gf.check_events(PARAM)
        if PARAM.stats.game_active:
            PARAM.ship.update()
            gf.update_bullets(PARAM)
            gf.update_aliens(PARAM)
        gf.update_screen(PARAM)
        await asyncio.sleep(0.00001)


# мое_
async def run_game():
    PARAMETERS= Parameters()
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    stars = create_stars(ai_settings, screen)
    play_button = Button(ai_settings, screen, "Play")
    pygame.display.set_caption(ai_settings.caption)
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    PARAMETERS.ai_settings = ai_settings
    PARAMETERS.screen = screen
    PARAMETERS.stars = stars
    PARAMETERS.play_button = play_button
    PARAMETERS.stats = stats
    PARAMETERS.sb = sb
    PARAMETERS.ship = ship
    PARAMETERS.bullets = bullets
    PARAMETERS.aliens = aliens
    gf.create_fleet(PARAMETERS)

    # мое
    # TODO сделать бегущую строку асинхронно. DONE!!!

    task1 = asyncio.create_task(
        main_loop(PARAMETERS))

    task2 = asyncio.create_task(caption_loop(ai_settings))
    await task1
    await task2


asyncio.run(run_game())
