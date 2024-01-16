import pyxel as px
import esper as es
from components.color import colors
from misc.logger import Logger


class BaseMenu:
    def __init__(self, game):
        self.game = game
        self.logger: Logger = game.logger
        self.level_name = ""
        self.menu = True
        self.star_colors = {
            "fastest_stars": "RED",
            "fast_stars": "GRAY",
            "slow_stars": "YELLOW",
            "slowest_stars": "ORANGE",
        }

    def menu_update(self):
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
                        self.logger.Log("Starting game...")
                        es.dispatch_event("select_level", "Ship Selection")
                    elif key == "settings":
                        es.dispatch_event("select_level", "Settings Menu", True)
                    elif key == "quit":
                        self.logger.Log("Quitting...")
                        px.quit()
                    break

    def menu_render(self):
        px.rect(14, 16, 38, 32, colors["BLACK"])
        px.rectb(14, 16, 38, 32, colors["WHITE"])
        px.text(18, 20, "Start", self.selection_color["start"])
        px.text(18, 28, "Settings", self.selection_color["settings"])
        px.text(18, 36, "Quit", self.selection_color["quit"])


class BaseLevel:
    def __init__(self, game):
        self.game = game
        self.logger: Logger = game.logger
        self.level_name = ""
        self.menu = False
        self.menu_showing = False
        self.selection_color = {
            "restart": colors["RED"],
            "settings": colors["WHITE"],
            "quit": colors["WHITE"],
        }
        self.player = []
        self.assets = []
        self.spawn_schedule = []
        self.star_colors = {
            "fastest_stars": "WHITE",
            "fast_stars": "LIGHT_BLUE",
            "slow_stars": "GRAY",
            "slowest_stars": "DARK_BLUE",
        }

    def menu_update(self):
        if not self.menu_showing:
            return

        # unpause game will only able to be called when paused
        if px.btn(px.KEY_P) and self.game.keypress_delay <= 0.0:
            es.dispatch_event("disable_pause")
            self.logger.Log(f"Paused: {self.game.paused}")
            self.game.keypress_delay = 25.0
            return

        if px.btnp(px.KEY_DOWN):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    self.selection_color[key] = colors["WHITE"]
                    if key == "restart":
                        self.selection_color["settings"] = colors["RED"]
                    elif key == "settings":
                        self.selection_color["quit"] = colors["RED"]
                    elif key == "quit":
                        self.selection_color["restart"] = colors["RED"]
                    break
        elif px.btnp(px.KEY_UP):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    self.selection_color[key] = colors["WHITE"]
                    if key == "restart":
                        self.selection_color["quit"] = colors["RED"]
                    elif key == "settings":
                        self.selection_color["restart"] = colors["RED"]
                    elif key == "quit":
                        self.selection_color["settings"] = colors["RED"]
                    break
        if px.btnp(px.KEY_RETURN):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    if key == "restart":
                        es.dispatch_event("restart_game")
                    elif key == "settings":
                        pass
                    elif key == "quit":
                        self.logger.Log("Quitting...")
                        px.quit()
                    break

    def menu_render(self):
        if not self.menu_showing:
            return

        px.text(20, 8, "Paused!", colors["ORANGE"])

        px.rect(14, 16, 38, 32, colors["BLACK"])
        px.rectb(14, 16, 38, 32, colors["WHITE"])
        px.text(18, 20, "Restart", self.selection_color["restart"])
        px.text(18, 28, "Settings", self.selection_color["settings"])
        px.text(18, 36, "Quit", self.selection_color["quit"])
