import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from explode import Explode


explode = None


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        sb.text_color = (255, 30, 30)
        stats.high_score = stats.score
        sb.prep_high_score()


def ship_hit(PARAM):
    # Уменьшение ships_left.
    if PARAM.stats.ships_left > 0:
        PARAM.stats.ships_left -= 1
        PARAM.sb.prep_ships()
        # Очистка списков пришельцев и пуль.
        PARAM.aliens.empty()
        PARAM.bullets.empty()
        # Создание нового флота и размещение корабля в центре.
        create_fleet(PARAM)
        PARAM.ship.center_ship()
        # Пауза.
        sleep(0.5)
    else:
        PARAM.stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(PARAM):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""
    global explode
    screen_rect = PARAM.screen.get_rect()
    for alien in PARAM.aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении с кораблем.
            explode = Explode(PARAM.ai_settings, PARAM.screen)
            explode.rect.x = PARAM.ship.rect.x
            explode.rect.y = PARAM.ship.rect.y
            ship_hit(PARAM)
            break


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    alien.rect.x = alien.x
    aliens.add(alien)


def create_fleet(PARAM):
    # Создание пришельца и вычисление количества пришельцев в ряду.
    alien = Alien(PARAM.ai_settings, PARAM.screen)
    number_aliens_x = get_number_aliens_x(PARAM.ai_settings, alien.rect.width)
    number_rows = get_number_rows(PARAM.ai_settings, PARAM.ship.rect.height,
                                  alien.rect.height)
    # Создание первого ряда пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(PARAM.ai_settings, PARAM.screen, PARAM.aliens, alien_number,
                         row_number)


def check_bullet_alien_collisions(PARAM):
    collisions = pygame.sprite.groupcollide(PARAM.bullets, PARAM.aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            PARAM.stats.score += PARAM.ai_settings.alien_points * len(aliens)
        PARAM.sb.prep_score()
        check_high_score(PARAM.stats, PARAM.sb)


def update_bullets(PARAM):

    for bullet in PARAM.bullets.copy():
        if bullet.rect.bottom <= 0:
            PARAM.bullets.remove(bullet)
    check_bullet_alien_collisions(PARAM)
    if len(PARAM.aliens) == 0:
        # Уничтожение существующих пуль и создание нового флота.
        PARAM.bullets.empty()
        PARAM.ai_settings.increase_speed()
        PARAM.stats.level += 1
        PARAM. sb.prep_level()
        create_fleet(PARAM)
    PARAM.bullets.update()


def update_aliens(PARAM):
    global explode
    check_fleet_edges(PARAM.ai_settings, PARAM.aliens)
    PARAM.aliens.update()

    if pygame.sprite.spritecollideany(PARAM.ship, PARAM.aliens):
        explode = Explode(PARAM.ai_settings, PARAM.screen)
        explode.rect.x = PARAM.ship.rect.x
        explode.rect.y = PARAM.ship.rect.y
        ship_hit(PARAM)
    check_aliens_bottom(PARAM)


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def fire_bullet(PARAM):
    # Создание новой пули и включение ее в группу bullets.
    if len(PARAM.bullets) < PARAM.ai_settings.bullets_allowed:
        new_bullet = Bullet(PARAM.ai_settings, PARAM.screen, PARAM.ship)
        PARAM.bullets.add(new_bullet)
    # мое
    # new_bullet2 = Bullet(ai_settings, screen, ship)
    # new_bullet2.rect.y = ship.rect.y + 30
    # new_bullet2.y = ship.rect.y + 30
    #
    # bullets.add(new_bullet2)
    # мое_


def check_keydown_events(event, PARAM):
    if event.key == pygame.K_RIGHT:
        PARAM.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        PARAM.ship.moving_left = True
    # мое
    elif event.key == pygame.K_UP:
        PARAM.ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        PARAM.ship.moving_down = True
    # мое_
    elif event.key == pygame.K_SPACE:
        fire_bullet(PARAM)
    elif event.key == pygame.K_q:
        PARAM.stats.write_record()
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    # мое
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    # мое_


def check_events(PARAM):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, PARAM)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, PARAM.ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(PARAM, mouse_x, mouse_y)


def check_play_button(PARAM, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = PARAM.play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not PARAM.stats.game_active:
        PARAM.ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        PARAM.stats.game_active = True

        PARAM.stats.reset_stats()
        # мое
        PARAM.sb.text_color = (30, 30, 30)
        # мое_

        PARAM.sb.prep_score()
        PARAM.sb.prep_high_score()
        PARAM.sb.prep_level()
        PARAM.sb.prep_ships()
        PARAM.aliens.empty()
        PARAM.bullets.empty()
        create_fleet(PARAM)
        PARAM.ship.center_ship()


def update_screen(PARAM):
    global explode
    if explode:
        explode.blitme()
        pygame.display.flip()
        sleep(0.5)
        explode.rect.x = 1000
        explode.rect.y = 1000
        explode = None

    PARAM.screen.fill(PARAM.ai_settings.bg_color)
    for star in PARAM.stars:
        star.draw_star()
    for bullet in PARAM.bullets.sprites():
        bullet.draw_bullet()
    PARAM.ship.blitme()
    PARAM.aliens.draw(PARAM.screen)
    PARAM.sb.show_score()
    if not PARAM.stats.game_active:
        PARAM.play_button.draw_button()

    pygame.display.flip()
