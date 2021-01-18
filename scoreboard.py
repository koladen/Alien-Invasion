import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard():
    """Класс для вывода игровой информации."""
    def __init__(self, ai_settings, screen, stats):
        """Инициализирует атрибуты подсчета очков."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # Настройки шрифта для вывода счета.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка исходного изображения.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        target = 'self.stats.score'
        text = "Счет: "
        self.prep(target, text, self.stats.score)

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        target = 'self.stats.high_score'
        text = "Рекорд: "
        self.prep(target, text, self.stats.high_score)

    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        target = 'self.stats.level'
        text = f"Уровень: {str(self.stats.level)}"
        self.prep(target, text, self.stats.level)

    def prep(self, target, text, number):
        rounded_score = round(number, -1)
        score_str = text + f"{rounded_score}"
        if target == 'self.stats.score':
            self.score_image = self.create_score_image(score_str)
            self.score_rect = self.score_image.get_rect()
            self.score_rect.right = self.screen_rect.right - 20
            self.score_rect.top = 20
        elif target == 'self.stats.high_score':
            self.high_score_image = self.create_score_image(score_str)
            self.high_score_rect = self.high_score_image.get_rect()
            self.high_score_rect.centerx = self.screen_rect.centerx
            self.high_score_rect.top = self.score_rect.top
        elif target == 'self.stats.level':
            self.level_image = self.create_score_image(text)
            self.level_rect = self.level_image.get_rect()
            self.level_rect.right = self.score_rect.right
            self.level_rect.top = self.score_rect.bottom + 10

    def create_score_image(self, score_str):
        return self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)


    def show_score(self):
        """Выводит счет на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_ships(self):
        """Сообщает количество оставшихся кораблей."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
