import pyxel as px
from level_loader.base import BaseLevel


class StartMenu(BaseLevel):
    def __init__(self, game):
        super().__init__(game)
        self.level_name = "start_menu"
        self.menu = True
        self.buttons = {
            "start": {"text": "Start", "x": 0, "y": 0},
            "settings": {"text": "Settings", "x": 0, "y": 8},
            "quit": {"text": "Quit", "x": 0, "y": 16},
        }

    def menu_function(self):
        # A menu function that loads/renders the start menu
        px.rect(16, 16, 48, 48, 7)
        px.text(20, 20, "Start", 0)
        px.text(20, 28, "Settings", 0)
        px.text(20, 36, "Quit", 0)

        # TODO: Figure out how to make the menu buttons work
