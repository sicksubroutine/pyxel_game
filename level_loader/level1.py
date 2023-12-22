import glm
from misc.logger import Logger
from components.transform import Transform
from components.velocity import Velocity
from components.collider import Collider
from components.health import Health
from components.sprite import Sprite, SpriteLayer
from components.keyboard_controller import KeyboardController
from components.projectile_emitter import ProjectileEmitter
from level_loader.base import BaseLevel


class Level1(BaseLevel):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.logger: Logger = game.logger
        self.menu = True
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
            Sprite(
                width=8,
                height=8,
                img=0,
                default_u=8,
                u=8,
                v=8,
                layer=SpriteLayer.PLAYER_LAYER,
                is_fixed=False,
            ),
            ProjectileEmitter(is_friendly=True, hit_damage=100),
        ]
        self.assets = [
            {
                "asset_type": "resource",
                "asset_id": "assets",
                "path": "./assets/assets.pyxres",
            },
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
                "enemy": "boss1",
                "x": 25,
                "y": -25,
                "velocity": 1.5,
                "health": 500,
                "delay": 0,
            },
            {
                "enemy": "boss2",
                "x": 50,
                "y": -25,
                "velocity": 1.5,
                "health": 1000,
                "delay": 500,
            },
            {
                "enemy": "boss3",
                "x": 60,
                "y": -25,
                "velocity": 1.5,
                "health": 1500,
                "delay": 1000,
            },
            {
                "enemy": "boss4",
                "x": 0,
                "y": -25,
                "velocity": 1.5,
                "health": 2000,
                "delay": 2000,
            },
            {
                "enemy": "boss1",
                "x": 15,
                "y": -25,
                "velocity": 1.5,
                "health": 2500,
                "delay": 3000,
            },
            {
                "enemy": "boss2",
                "x": 25,
                "y": 5,
                "velocity": 1.5,
                "health": 3000,
                "delay": 4000,
            },
        ]
