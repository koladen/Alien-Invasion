import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.center_y = float(self.rect.centery)

        self.moving_right = False
        self.moving_left = False

        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right:
            self.move_right()

        if self.moving_left:
            self.move_left()

        if self.moving_up:
            self.move_up()

        if self.moving_down:
            self.move_down()

        self.rect.centerx = self.center
        self.rect.centery = self.center_y

    def move_right(self):
        if self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

    def move_left(self):
        if self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

    def move_up(self):
        if self.rect.top > self.screen_rect.top:
            self.center_y -= self.ai_settings.ship_speed_factor

    def move_down(self):
        if self.rect.bottom < self.screen_rect.bottom:
            self.center_y += self.ai_settings.ship_speed_factor

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.center = self.screen_rect.centerx
        self.center_y = self.screen_rect.bottom-self.rect.height/2

