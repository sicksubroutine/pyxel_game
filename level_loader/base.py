class BaseLevel:
    def __init__(self, game):
        self.game = game
        self.level_name = ""
        self.menu = False
        self.player = []
        self.assets = []
        self.spawn_schedule = []
