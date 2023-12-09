import esper as es
import glm
from misc.entity import EntityPool
from misc.logger import Logger

from components.transform import Transform
from components.sprite import Sprite, SpriteLayer
from components.projectile_emitter import ProjectileEmitter
from components.velocity import Velocity
from components.projectile import Projectile
from components.collider import Collider


class ProjectileEmitterSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger

    def player_shoot(self):
        for ent, (transform, emitter) in es.get_components(
            Transform, ProjectileEmitter
        ):
            if emitter.is_active:
                emitter.is_active = False
                self.create_projectile(transform.position.x, transform.position.y)

    def create_projectile(self, x, y):
        transform = Transform(glm.vec2(x, y), glm.vec2(1, 1), 0.0)
        sprite = Sprite(3, 6, 1, 10, 9, SpriteLayer.BULLET_LAYER, False, True)
        collider = Collider(width=3, height=6, offset=glm.vec2(0, 0), group="bullet")
        proj = Projectile(
            duration=1.0,
            hit_damage=1,
            is_friendly=True,
            start_time=self.game.clock,
        )
        projectile = self.pool.create_entity(transform, sprite, collider)

    def process(self):
        for ent, (transform, emitter, sprite) in es.get_components(
            Transform, ProjectileEmitter, Sprite
        ):
            ...
