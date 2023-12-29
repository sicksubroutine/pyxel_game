from level_loader.base import BaseMenu
import pyxel as px
from misc.logger import Logger
from components.color import colors


class TransitionScreen(BaseMenu):
    def __init__(self, game, current_level):
        super().__init__(game)
        self.current_level = current_level
        self.menu = True

    def menu_update(self):
        ...

    def menu_render(self):
        px.rect(14, 16, 38, 18, colors["BLACK"])
        px.rectb(14, 16, 38, 18, colors["WHITE"])
        px.text(16, 18, f"{self.current_level}", colors["RED"])
        px.text(16, 26, "Complete!", colors["WHITE"])
