class GameStats():
    PATH = r'max_score'

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.game_active = False
        self.reset_stats()
        self.high_score = self.prep_highscore()

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    @staticmethod
    def prep_highscore():
        with open(GameStats.PATH, 'r') as f:
            return int(f.read())

    def write_record(self):
        with open(GameStats.PATH, 'w') as f:
            f.write(str(self.high_score))

