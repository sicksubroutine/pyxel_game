"""
A tool for building a Spawn Schedule that each level will contain.
It will be a graphical interface that will allow the user to place enemies depending on the "timer" of the level.

"""

import pyxel as px
import time
from glm import vec2
from misc.config import ConfigManager
from misc.logger import Logger
from misc.asset_store import AssetStore
from misc.entity import EntityPool
from dataclasses import dataclass

from level_loader.enemies import Enemies

from systems.star_system import StarSystem


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int


class BaseMode:
    def __init__(self, tool):
        self.tool = tool
        self.time = 0.0

    def check_mouse_click(self, mouse, rect):
        if rect.x < mouse.x < rect.x + rect.w and rect.y < mouse.y < rect.y + rect.h:
            return True
        return False

    def render(self): ...

    def update(self): ...


class SelectionMode(BaseMode):
    def __init__(self, tool):
        self.tool = tool
        self.ships = self.tool.ships
        self.selected_ship = tool.selected_ship

    def render(self):
        # put a red box around the selected ship while hovering
        # check if the mouse is within the rect of the ship
        mouse_pos = vec2(px.mouse_x, px.mouse_y)
        for ship in self.ships:
            if self.check_mouse_click(mouse_pos, self.ships[ship]["rect"]):
                px.rectb(
                    self.ships[ship]["rect"].x - 1,
                    self.ships[ship]["rect"].y - 1,
                    self.ships[ship]["rect"].w + 2,
                    self.ships[ship]["rect"].h + 2,
                    8,
                )
            # if ship is selected, keep the box around it
            if self.selected_ship == ship:
                px.rectb(
                    self.ships[ship]["rect"].x - 1,
                    self.ships[ship]["rect"].y - 1,
                    self.ships[ship]["rect"].w + 2,
                    self.ships[ship]["rect"].h + 2,
                    8,
                )
        px.text(0, 0, "Selection Mode", 7)
        for index, ship in enumerate(self.ships):
            px.blt(
                10,
                10 + (10 * index),
                0,
                self.ships[ship]["u"],
                self.ships[ship]["v"],
                8,
                8,
                0,
            )

    def update(self):
        mouse_pos = vec2(px.mouse_x, px.mouse_y)
        if px.btnp(px.MOUSE_BUTTON_LEFT):
            for ship in self.ships:
                if self.check_mouse_click(mouse_pos, self.ships[ship]["rect"]):
                    print(f"Selected ship: {ship}")
                    self.tool.selected_ship = ship
                    self.tool.logger.Log(f"Selected ship: {self.selected_ship}")


class PlacementMode(BaseMode):
    def __init__(self, tool):
        self.tool = tool
        self.ships = self.tool.ships
        self.selected_ship = tool.selected_ship

    def render(self):
        px.text(0, 0, "Placement Mode", 7)
        for index, ship in enumerate(self.ships):
            px.blt(
                10,
                10 + (10 * index),
                0,
                self.ships[ship]["u"],
                self.ships[ship]["v"],
                8,
                8,
                0,
            )

    def update(self): ...

    def advance_time(self):
        # A method that will advance the time by 1 second
        # time is used as a way to separate the enemies in the spawn schedule
        self.time += 1.0

    def reverse_time(self):
        # A method that will reverse the time by 1 second
        # time is used as a way to separate the enemies in the spawn schedule
        self.time -= 1.0

    def set_time(self, time):
        # A method that will set the time to a specific value
        self.time = time

    def get_time(self):
        # A method that will return the current time
        return self.time

    def place_enemy(self, enemy):
        # A method that will place the enemy in the spawn schedule
        ...


class PreviewMode(BaseMode):
    def __init__(self, tool):
        self.tool = tool

    def render(self):
        px.text(0, 0, "Preview Mode", 7)

    def update(self):
        self.play_time_forward()

    def play_time_forward(self):
        self.time += 1.0


class Spawner:
    """Use this to create enemies for the Spawn Builder"""

    def __init__(self, tool):
        self.tool = tool
        self.logger: Logger = tool.logger

    def gen_enemy(self, enemy): ...


class SpawnBuilder:
    def __init__(self):
        self.config: ConfigManager = ConfigManager()
        self.logger: Logger = Logger(
            console_print=False,
            file_write=True,
            file_path="spawn_builder.txt",
        )
        self.asset_store: AssetStore = AssetStore(self)
        self.spawner = Spawner(self)
        self.enemies: Enemies = Enemies(self)
        self.pool: EntityPool = EntityPool(self)
        self.selected_ship = None
        self.ships = {
            "ship1": {"u": 8, "v": 0, "rect": Rect(10, 10, 8, 8)},
            "ship2": {"u": 8, "v": 8, "rect": Rect(10, 20, 8, 8)},
            "ship3": {"u": 8, "v": 16, "rect": Rect(10, 30, 8, 8)},
            "ship4": {"u": 8, "v": 24, "rect": Rect(10, 40, 8, 8)},
            "ship5": {"u": 8, "v": 32, "rect": Rect(10, 50, 8, 8)},
        }

        self.enemy_types = self.enemies.enemy_types

        self.res_width = self.config.window_width
        self.res_height = self.config.window_height
        self.fps = self.config.target_fps
        px.init(self.res_width, self.res_height, title="Spawn Builder", fps=self.fps)
        px.load("assets/assets.pyxres", True, True, True, True)
        self.logger.Log(f"Pyxel initialized at {self.res_width}x{self.res_height}")

        self.systems_setup()
        self.delay = 0.0

        # show mouse
        px.mouse(True)
        self.mouse_pos = vec2(px.mouse_x, px.mouse_y)
        # possible modes: placement, preview
        self.possible_modes = [
            {
                "name": "selection",
                "class": SelectionMode,
            },
            {
                "name": "placement",
                "class": PlacementMode,
            },
            {
                "name": "preview",
                "class": PreviewMode,
            },
        ]
        self.mode_index = 0
        self.tool_mode = self.possible_modes[self.mode_index]
        self.tool_class = self.possible_modes[self.mode_index]["class"](self)

    def mode_class_switch(self):
        self.tool_mode = self.possible_modes[self.mode_index]
        self.tool_class = self.possible_modes[self.mode_index]["class"](self)

    def mode_switcher(self):
        # change mode class
        try:
            self.mode_index += 1
            if self.mode_index > len(self.possible_modes) - 1:
                self.mode_index = 0
        except Exception as e:
            self.logger.Log(f"Error: {e}")

    def keyboard_controls(self):
        # switch mode using m key
        if px.btnp(px.KEY_M):
            self.mode_switcher()
        # print out the current selected ship if press p
        if px.btnp(px.KEY_P):
            print(f"Selected ship: {self.selected_ship}")

    def mouse_controls(self):
        self.mouse_pos = vec2(px.mouse_x, px.mouse_y)
        # # center mouse on screen
        # px.mouse_x = self.res_width // 2
        # px.mouse_y = self.res_height // 2

    def fps_counter(self):
        self.frames += 1
        new_now = time.perf_counter()
        if new_now - self.last_clock >= 1.0:
            self.fps = round(self.frames / (new_now - self.last_clock), 2)
            self.frames = 0
            self.last_clock = new_now

    def systems_setup(self):
        star_colors = {
            "fastest_stars": "WHITE",
            "fast_stars": "LIGHT_BLUE",
            "slow_stars": "GRAY",
            "slowest_stars": "DARK_BLUE",
        }
        self.star_system = StarSystem(star_colors)

    def update(self):
        self.current_mode_update = self.tool_class.update()
        self.mode_class_switch()
        self.star_system.update()
        # self.mouse_controls()
        self.keyboard_controls()

    def render(self):
        px.cls(0)
        self.star_system.render()
        # print the current mode on the screen
        self.current_mode_render = self.tool_class.render()

    def run(self):
        px.run(self.update, self.render)


if __name__ == "__main__":
    sb = SpawnBuilder()
    sb.run()
