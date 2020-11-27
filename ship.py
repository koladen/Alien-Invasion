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
# мое
        self.center_y = float(self.rect.centery)
# мое

        self.moving_right = False
        self.moving_left = False
        # мое
        self.moving_up = False
        self.moving_down = False
        # мое_

    def update(self):
        if self.moving_right:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor

        if self.moving_left:
            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center
# мое
        if self.moving_up:
            if self.moving_up and self.rect.top > self.screen_rect.top:
                self.center_y -= self.ai_settings.ship_speed_factor

        if self.moving_down:
            if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
                self.center_y += self.ai_settings.ship_speed_factor

        self.rect.centery = self.center_y
# мое_

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.center = self.screen_rect.centerx
        self.center_y = self.screen_rect.bottom-self.rect.height/2

