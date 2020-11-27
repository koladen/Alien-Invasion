import pygame
from pygame.sprite import Sprite
import random


class Star(Sprite):
    def __init__(self, ai_settings, screen):
        super() .__init__()
        self.screen = screen
        star_size = random.randrange(1, 5)
        self.rect = pygame.Rect(random.randrange(ai_settings.screen_width), random.randrange(ai_settings.screen_height),
                                star_size, star_size)
        self.color = random.choice(ai_settings.star_colors)

    def draw_star(self):
        pygame.draw.rect(self.screen, self.color, self.rect)