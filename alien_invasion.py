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


def create_stars(ai_settings, screen):
    return [Star(ai_settings, screen) for _ in range(ai_settings.star_count)]


# мое
async def caption_loop():
    ai_settings = Settings()
    while True:
        for i in range(len(ai_settings.caption)):
            pygame.display.set_caption(ai_settings.caption[i + 1:] + ' ' + ai_settings.caption[0:i+1])
            await asyncio.sleep(0.02)


async def main_loop(ai_settings, screen, stats, sb, play_button, ship, bullets, aliens, stars):
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                             bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         bullets, stars, play_button)
        await asyncio.sleep(0.00001)


# мое_
async def run_game():
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
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # мое
    # TODO сделать бегущую строку асинхронно. DONE!!!

    task1 = asyncio.create_task(
        main_loop(ai_settings, screen, stats, sb, play_button, ship, bullets, aliens, stars))

    task2 = asyncio.create_task(caption_loop())
    await task1
    await task2


asyncio.run(run_game())
