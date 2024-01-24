import glm
from components.transform import Transform
from components.velocity import Velocity
from components.collider import Collider
from components.health import Health
from components.keyboard_controller import KeyboardController
from components.projectile_emitter import ProjectileEmitter
from level_loader.base import BaseLevel


class Level3(BaseLevel):
    def __init__(self, game):
        super().__init__(game)
        self.level_name = "level 3"
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
            ProjectileEmitter(is_friendly=True, hit_damage=25),
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
                "enemy": "white_guy",
                "x": 25,
                "y": -25,
                "velocity": 0.15,
                "delay": 0,
            }
        ]
        self.star_colors = {
            "fastest_stars": "VIOLET",
            "fast_stars": "LIGHT_BLUE",
            "slow_stars": "LIME_GREEN",
            "slowest_stars": "ORANGE",
        }
