from level_loader.base import BaseMenu
from misc.logger import Logger
from components.color import colors
import glm


class StartMenu(BaseMenu):
    def __init__(self, game):
        super().__init__(game)
        self.level_name = "Start Menu"
        self.menu = True
        self.selection_color = {
            "start": colors["RED"],
            "settings": colors["WHITE"],
            "quit": colors["WHITE"],
        }
