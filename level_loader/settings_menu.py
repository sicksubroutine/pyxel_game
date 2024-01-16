from level_loader.base import BaseMenu
from components.color import colors
import pyxel as px
import esper as es


class SettingsMenu(BaseMenu):
    def __init__(self, game):
        super().__init__(game)
        self.level_name = "Settings Menu"
        self.menu = True
        self.selection_color = {
            "fps": colors["WHITE"],
            "width": colors["WHITE"],
            "height": colors["WHITE"],
            "back": colors["RED"],
        }

    def menu_update(self):
        if px.btnp(px.KEY_DOWN):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    self.selection_color[key] = colors["WHITE"]
                    if key == "fps":
                        self.selection_color["width"] = colors["RED"]
                    elif key == "width":
                        self.selection_color["height"] = colors["RED"]
                    elif key == "height":
                        self.selection_color["back"] = colors["RED"]
                    elif key == "back":
                        self.selection_color["fps"] = colors["RED"]
                    break
        elif px.btnp(px.KEY_UP):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    self.selection_color[key] = colors["WHITE"]
                    if key == "fps":
                        self.selection_color["back"] = colors["RED"]
                    elif key == "width":
                        self.selection_color["fps"] = colors["RED"]
                    elif key == "height":
                        self.selection_color["width"] = colors["RED"]
                    elif key == "back":
                        self.selection_color["height"] = colors["RED"]
                    break
        if px.btnp(px.KEY_RETURN):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    if key == "fps":
                        es.dispatch_event("select_level", "FPS Select", True)
                    elif key == "width":
                        es.dispatch_event("select_level", "Resolution Select", True)
                    elif key == "height":
                        es.dispatch_event("select_level", "Resolution Select", True)
                    elif key == "back":
                        es.dispatch_event("select_level", "Start Menu")
                    break

    def menu_render(self):
        px.rect(14, 16, 38, 38, colors["BLACK"])
        px.rectb(14, 16, 38, 38, colors["WHITE"])
        px.text(18, 20, "FPS", self.selection_color["fps"])
        px.text(18, 28, "width", self.selection_color["width"])
        px.text(18, 36, "height", self.selection_color["height"])
        px.text(18, 44, "back", self.selection_color["back"])


class FPSSelect(BaseMenu):
    def __init__(self, game):
        super().__init__(game)
        self.level_name = "FPS Select"
        self.menu = True
        self.selection_color = {
            "30": colors["WHITE"],
            "60": colors["WHITE"],
            "back": colors["RED"],
        }

    @staticmethod
    def fps_change(value):
        file_path = "misc/config.py"
        with open(file_path, "r") as f:
            lines = f.readlines()
        with open(file_path, "w") as f:
            for line in lines:
                if "target_fps" in line:
                    line = f"    target_fps: int = {value}\n"
                f.write(line)

    def menu_update(self):
        if px.btnp(px.KEY_DOWN):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    self.selection_color[key] = colors["WHITE"]
                    if key == "30":
                        self.selection_color["60"] = colors["RED"]
                    elif key == "60":
                        self.selection_color["back"] = colors["RED"]
                    elif key == "back":
                        self.selection_color["30"] = colors["RED"]
                    break
        elif px.btnp(px.KEY_UP):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    self.selection_color[key] = colors["WHITE"]
                    if key == "30":
                        self.selection_color["back"] = colors["RED"]
                    elif key == "60":
                        self.selection_color["30"] = colors["RED"]
                    elif key == "back":
                        self.selection_color["60"] = colors["RED"]
                    break
        if px.btnp(px.KEY_RETURN):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    if key == "30":
                        self.fps_change(30)
                        self.logger.Log("FPS changed to 30")
                    elif key == "60":
                        self.fps_change(60)
                        self.logger.Log("FPS changed to 60")
                    elif key == "back":
                        es.dispatch_event("select_level", "Settings Menu")
                    break

    def menu_render(self):
        px.rect(14, 16, 38, 38, colors["BLACK"])
        px.rectb(14, 16, 38, 38, colors["WHITE"])
        px.text(18, 20, "30", self.selection_color["30"])
        px.text(18, 28, "60", self.selection_color["60"])
        px.text(18, 36, "back", self.selection_color["back"])


class ResolutionSelect(BaseMenu):
    def __init__(self, game):
        super().__init__(game)
        self.level_name = "Resolution Select"
        self.menu = True
        self.selection_color = {
            "width": colors["WHITE"],
            "height": colors["WHITE"],
            "back": colors["RED"],
        }

    def menu_update(self):
        if px.btnp(px.KEY_DOWN):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    self.selection_color[key] = colors["WHITE"]
                    if key == "width":
                        self.selection_color["height"] = colors["RED"]
                    elif key == "height":
                        self.selection_color["back"] = colors["RED"]
                    elif key == "back":
                        self.selection_color["width"] = colors["RED"]
                    break
        elif px.btnp(px.KEY_UP):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    self.selection_color[key] = colors["WHITE"]
                    if key == "width":
                        self.selection_color["back"] = colors["RED"]
                    elif key == "height":
                        self.selection_color["width"] = colors["RED"]
                    elif key == "back":
                        self.selection_color["height"] = colors["RED"]
                    break
        if px.btnp(px.KEY_RETURN):
            for key in self.selection_color:
                if self.selection_color[key] == colors["RED"]:
                    if key == "width":
                        ...
                    elif key == "height":
                        ...
                    elif key == "back":
                        es.dispatch_event("select_level", "Settings Menu")
                    break

    def menu_render(self):
        px.rect(14, 16, 38, 38, colors["BLACK"])
        px.rectb(14, 16, 38, 38, colors["WHITE"])
        px.text(18, 20, "width", self.selection_color["width"])
        px.text(18, 28, "height", self.selection_color["height"])
        px.text(18, 36, "back", self.selection_color["back"])
