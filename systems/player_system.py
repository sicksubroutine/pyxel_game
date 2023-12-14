from components.transform import Transform
from components.velocity import Velocity
from components.keyboard_controller import KeyboardController
from components.collider import Collider
from components.color import Color, Colors
from components.sprite import Sprite, SpriteLayer
from components.projectile_emitter import ProjectileEmitter
from components.health import Health
import glm
from misc.entity import EntityPool, Entity
from misc.logger import Logger


class PlayerSystem:
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger
        self.player: Entity = None

    def player_setup(self):
        sprite = Sprite(
            width=8,
            height=8,
            img=0,
            default_u=8,
            u=8,
            v=8,
            layer=SpriteLayer.PLAYER_LAYER,
            is_fixed=False,
        )
        color = Color(color=Colors.RED)
        transform = Transform(
            position=glm.vec2(25, 50), scale=glm.vec2(5, 5), rotation=0.0
        )
        velocity = Velocity(velocity=glm.vec2(0, 0))
        keyboard = KeyboardController(
            glm.vec2(0, -1),
            glm.vec2(1, 0),
            glm.vec2(0, 1),
            glm.vec2(-1, 0),
        )
        health = Health(100, 100, False)
        collider = Collider(width=8, height=8, offset=glm.vec2(0, 0), group="player")
        proj_emitter = ProjectileEmitter(is_friendly=True, hit_damage=10)
        self.player: Entity = self.pool.create_entity(
            transform,
            velocity,
            keyboard,
            color,
            collider,
            sprite,
            proj_emitter,
            health,
        )
        self.player.Group("player")
        return self.player

    def player_death(self):
        self.pool.remove_entity(self.player)

    def respawn_player(self):
        self.player = self.player_setup()
