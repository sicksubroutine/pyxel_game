from level_loader.base import BaseMenu
import pyxel as px
from misc.logger import Logger
from components.color import colors

# TODO: This screen will show up when the player completes a level.
# It will temporarily replace the "menu_update/menu_render" methods.


class TransitionScreen(BaseMenu):
    def __init__(self, game):
        super().__init__(game)

    def menu_update(self):
        ...

    def menu_draw(self):
        px.rect(14, 16, 38, 32, colors["BLACK"])
        px.rectb(14, 16, 38, 32, colors["WHITE"])
