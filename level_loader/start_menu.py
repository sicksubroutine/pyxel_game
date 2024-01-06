from level_loader.base import BaseMenu
from misc.logger import Logger
from components.color import colors
import glm


class StartMenu(BaseMenu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.logger: Logger = game.logger
        self.level_name = "Start Menu"
        self.menu = True
        self.mouse: glm.vec2 = glm.vec2(0, 0)
        self.selection_color = {
            "start": colors["RED"],
            "settings": colors["WHITE"],
            "quit": colors["WHITE"],
        }

    def settings_menu_init(self):
        self.selection_color = {
            "fps": colors["WHITE"],
            "width": colors["WHITE"],
            "height": colors["WHITE"],
        }

    def settings_menu_update(self):
        ...

    def settings_menu_render(self):
        ...
