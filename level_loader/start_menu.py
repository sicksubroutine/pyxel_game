import pyxel as px
import esper as es
from level_loader.base import BaseLevel
from misc.logger import Logger
import glm


class StartMenu(BaseLevel):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.logger: Logger = game.logger
        self.level_name = "Start Menu"
        self.menu = True
        self.menu_showing = True
        self.mouse: glm.vec2 = glm.vec2(0, 0)

    def menu_update(self):
        # mouse control
        # self.mouse = glm.vec2(px.mouse_x, px.mouse_y)

        # if px.btnp(px.MOUSE_BUTTON_LEFT):
        #     if self.mouse.x > 18 and self.mouse.x < 54:
        #         if self.mouse.y > 20 and self.mouse.y < 28:
        #             es.dispatch_event("start_game")
        #         elif self.mouse.y > 28 and self.mouse.y < 36:
        #             pass
        #         elif self.mouse.y > 36 and self.mouse.y < 44:
        #             self.logger.Log("Quitting...")
        #             px.quit()

        if px.btnp(px.KEY_DOWN):
            for key in self.selection_color:
                if self.selection_color[key] == self.colors["RED"]:
                    self.selection_color[key] = self.colors["WHITE"]
                    if key == "start":
                        self.selection_color["settings"] = self.colors["RED"]
                    elif key == "settings":
                        self.selection_color["quit"] = self.colors["RED"]
                    elif key == "quit":
                        self.selection_color["start"] = self.colors["RED"]
                    break
        elif px.btnp(px.KEY_UP):
            for key in self.selection_color:
                if self.selection_color[key] == self.colors["RED"]:
                    self.selection_color[key] = self.colors["WHITE"]
                    if key == "start":
                        self.selection_color["quit"] = self.colors["RED"]
                    elif key == "settings":
                        self.selection_color["start"] = self.colors["RED"]
                    elif key == "quit":
                        self.selection_color["settings"] = self.colors["RED"]
                    break
        if px.btnp(px.KEY_RETURN):
            for key in self.selection_color:
                if self.selection_color[key] == self.colors["RED"]:
                    if key == "start":
                        es.dispatch_event("start_game")
                    elif key == "settings":
                        pass
                    elif key == "quit":
                        self.logger.Log("Quitting...")
                        px.quit()
                    break
