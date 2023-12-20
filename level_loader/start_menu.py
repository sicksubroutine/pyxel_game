import pyxel as px
import esper as es
from level_loader.base import BaseLevel
from misc.logger import Logger
from components.color import Colors
import glm

colors = {color: Colors[color].value for color in Colors.__members__}


class StartMenu(BaseLevel):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.logger: Logger = game.logger
        self.level_name = "start_menu"
        self.menu = True
        self.buttons = {
            "start": {"text": "Start", "x": 0, "y": 0},
            "settings": {"text": "Settings", "x": 0, "y": 8},
            "quit": {"text": "Quit", "x": 0, "y": 18},
        }
        self.selection_color = {
            "start": colors["RED"],
            "settings": colors["WHITE"],
            "quit": colors["WHITE"],
        }
        self.mouse: glm.vec2 = glm.vec2(0, 0)

    def menu_render(self):
        # draw mouse cursor
        px.blt(self.mouse.x, self.mouse.y, 0, 0, 0, 2, 2, colors["BLACK"])
        # A menu function that loads/renders the start menu
        px.rect(14, 16, 38, 32, colors["BLACK"])
        px.rectb(14, 16, 38, 32, colors["WHITE"])
        px.text(18, 20, "Start", self.selection_color["start"])
        px.text(18, 28, "Settings", self.selection_color["settings"])
        px.text(18, 36, "Quit", self.selection_color["quit"])

    def menu_update(self):
        # mouse control
        self.mouse = glm.vec2(px.mouse_x, px.mouse_y)

        if px.btnp(px.MOUSE_BUTTON_LEFT):
            if self.mouse.x > 18 and self.mouse.x < 54:
                if self.mouse.y > 20 and self.mouse.y < 28:
                    es.dispatch_event("start_game")
                elif self.mouse.y > 28 and self.mouse.y < 36:
                    pass
                elif self.mouse.y > 36 and self.mouse.y < 44:
                    self.logger.Log("Quitting...")
                    px.quit()

        if px.btnp(px.KEY_DOWN):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    self.selection_color[key] = colors["WHITE"]
                    if key == "start":
                        self.selection_color["settings"] = colors["RED"]
                    elif key == "settings":
                        self.selection_color["quit"] = colors["RED"]
                    elif key == "quit":
                        self.selection_color["start"] = colors["RED"]
                    break
        elif px.btnp(px.KEY_UP):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    self.selection_color[key] = colors["WHITE"]
                    if key == "start":
                        self.selection_color["quit"] = colors["RED"]
                    elif key == "settings":
                        self.selection_color["start"] = colors["RED"]
                    elif key == "quit":
                        self.selection_color["settings"] = colors["RED"]
                    break
        if px.btnp(px.KEY_RETURN):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    if key == "start":
                        es.dispatch_event("start_game")
                    elif key == "settings":
                        pass
                    elif key == "quit":
                        self.logger.Log("Quitting...")
                        px.quit()
                    break
