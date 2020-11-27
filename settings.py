class Settings():
    def __init__(self):
        # Настройки экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.caption = 'Инопланетное вторжение' + ' '*200
        self.bg_color = (230, 230, 230)
        # Настройки корабля

        self.ship_limit = 3
        # Настройки пуль

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 3
        # Настройки звезд
        self.star_colors = [(255, 179, 0), (0, 0, 255), (0, 255, 0), (255, 160, 122),
                            (255, 105, 180), (255, 140, 0), (188, 143, 143), (50, 205, 50), (30, 144, 255)]
        self.star_count = 1000
        # Настройки пришельцев

        self.fleet_drop_speed = 10
        # Темп ускорения игры
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 0.5
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
