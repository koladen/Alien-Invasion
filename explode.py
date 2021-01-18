import pygame
from pygame.sprite import Sprite


class Explode(Sprite):
    count = 0

    def __init__(self, ai_settings, screen):
        self.__class__.count += 1
        super(Explode, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/explozion.bmp')
        self.rect = self.image.get_rect()
        self.color = 255, 0, 0

    def draw_explode(self, rect):
        pygame.draw.rect(self.screen, self.color, rect)

    def blitme(self):
        self.screen.blit(self.image, self.rect)


