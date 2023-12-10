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
            self.create_projectile(
                transform.position.x + 2,
                transform.position.y + 1,
                emitter.is_friendly,
            )

    def create_projectile(self, x, y, is_friendly):
        transform = Transform(glm.vec2(x, y), glm.vec2(1, 1), 0.0)
        velocity = Velocity(velocity=glm.vec2(0, -1))
        sprite = Sprite(3, 6, 1, 10, 9, SpriteLayer.BULLET_LAYER, False, True)
        collider = Collider(width=3, height=6, offset=glm.vec2(0, 0), group="bullet")
        proj = Projectile(
            duration=100.0, hit_damage=1, is_friendly=is_friendly, start_time=0.0
        )
        projectile = self.pool.create_entity(
            transform, sprite, collider, velocity, proj
        )
        projectile.Group("bullet")

    def process(self):
        for ent, (transform, emitter, sprite) in es.get_components(
            Transform, ProjectileEmitter, Sprite
        ):
            ...


class ProjectileLifetimeSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger
        self.timer = 0.0

    def process(self):
        self.timer += 1.0
        for ent, (transform, projectile) in es.get_components(Transform, Projectile):
            if projectile.start_time == 0.0:
                projectile.start_time = self.timer
            if self.timer - projectile.start_time >= projectile.duration:
                self.pool.remove_entity(ent)
