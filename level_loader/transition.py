from level_loader.base import BaseMenu
import pyxel as px
from misc.logger import Logger
from components.color import colors

# TODO: This screen will show up when the player completes a level.
# It will temporarily replace the "menu_update/menu_render" methods.


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
        px.text(16, 18, f"Level {self.current_level}", colors["RED"])
        px.text(16, 26, "Complete!", colors["WHITE"])
