import glm
import pyxel as px
import esper as es
from misc.logger import Logger
from components.transform import Transform
from components.velocity import Velocity
from components.collider import Collider
from components.health import Health
from components.keyboard_controller import KeyboardController
from components.projectile_emitter import ProjectileEmitter
from level_loader.base import BaseLevel


class Level1(BaseLevel):
    def __init__(self, game):
        super().__init__(game)
        self.level_name = "level 1"
        self.player = [
            Transform(position=glm.vec2(25, 50), scale=glm.vec2(5, 5), rotation=0.0),
            Velocity(velocity=glm.vec2(0, 0)),
            KeyboardController(
                glm.vec2(0, -1),
                glm.vec2(1, 0),
                glm.vec2(0, 1),
                glm.vec2(-1, 0),
            ),
            Health(max_health=100, current_health=100, is_god_mode=False),
            Collider(width=8, height=8, offset=glm.vec2(0, 0), group="player"),
            ProjectileEmitter(is_friendly=True, hit_damage=100),
        ]
        self.assets = [
            {
                "asset_type": "sound",
                "asset_id": "shoot",
                "number": 0,
            },
            {
                "asset_type": "sound",
                "asset_id": "hit",
                "number": 1,
            },
            {
                "asset_type": "sound",
                "asset_id": "explode",
                "number": 2,
            },
        ]

        self.spawn_schedule = [
            {
                "enemy": "green_guy",
                "x": 25,
                "y": -25,
                "velocity": 0.00,
                "health": 300,
                "delay": 0,
            },
            {
                "enemy": "green_guy",
                "x": 25,
                "y": -25,
                "velocity": 0.00,
                "health": 300,
                "delay": 40,
            },
            {
                "enemy": "green_guy",
                "x": 25,
                "y": -25,
                "velocity": 0.00,
                "health": 300,
                "delay": 80,
            },
            {
                "enemy": "red_guy",
                "x": 56,
                "y": -25,
                "velocity": 0.00,
                "health": 300,
                "delay": 150,
            },
            {
                "enemy": "red_guy",
                "x": 56,
                "y": -25,
                "velocity": 0.00,
                "health": 300,
                "delay": 190,
            },
            {
                "enemy": "red_guy",
                "x": 56,
                "y": -25,
                "velocity": 0.00,
                "health": 300,
                "delay": 230,
            },
            {
                "enemy": "white_guy",
                "x": 0,
                "y": -25,
                "velocity": 0.00,
                "health": 300,
                "delay": 300,
            },
            {
                "enemy": "white_guy",
                "x": 0,
                "y": -25,
                "velocity": 0.00,
                "health": 300,
                "delay": 340,
            },
            {
                "enemy": "white_guy",
                "x": 0,
                "y": -25,
                "velocity": 0.00,
                "health": 300,
                "delay": 380,
            },
        ]
