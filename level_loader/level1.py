import glm
from components.transform import Transform
from components.velocity import Velocity
from components.collider import Collider
from components.health import Health
from components.sprite import Sprite, SpriteLayer
from components.keyboard_controller import KeyboardController


class Level1:
    def __init__(self, game):
        self.level_name = "level1"
        self.player: {
            "transform": Transform(
                position=glm.vec2(25, 50), scale=glm.vec2(5, 5), rotation=0.0
            ),
            "velocity": Velocity(velocity=glm.vec2(0, 0)),
            "keyboard": KeyboardController(
                glm.vec2(0, -1),
                glm.vec2(1, 0),
                glm.vec2(0, 1),
                glm.vec2(-1, 0),
            ),
            "health": Health(max_health=100, current_health=100, is_god_mode=False),
            "collider": Collider(
                width=8, height=8, offset=glm.vec2(0, 0), group="player"
            ),
            "sprite": Sprite(
                width=8,
                height=8,
                img=0,
                default_u=8,
                u=8,
                v=8,
                layer=SpriteLayer.PLAYER_LAYER,
                is_fixed=False,
            ),
        }
        # TODO: Get around to making a spawn schedule
        self.spawn_schedule = {}
