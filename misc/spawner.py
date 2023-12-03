import esper as es
import random
import glm
import pygame as pg
from misc.entity import EntityPool
from components.transform import Transform
from components.velocity import Velocity
from components.sprite import Sprite, SpriteLayer
from components.collider import Collider
from components.health import Health
from components.projectile_emitter import ProjectileEmitter
from misc.logger import Logger


class Spawner:
    def __init__(self, pool: EntityPool, logger: Logger):
        self.pool: EntityPool = pool
        self.logger: Logger = logger
        self.logger.Log("Spawner initialized")

    def gen_random_entity(self, group, pos, scale, rot, vel, enemy_type) -> None:
        src_rect = pg.Rect(0, 0, 32, 32)
        layer = SpriteLayer.GROUND_LAYER
        projectile_velocity = glm.vec2(vel.x * 4, vel.y * 4)
        ent = self.pool.create_entity(
            Transform(pos, scale, rot),
            Velocity(vel),
            Collider(32, 32, glm.vec2(0, 0), group),
            Health(100, 100, False),
            Sprite(enemy_type, 32, 32, layer, False, src_rect),
            ProjectileEmitter(
                500,
                projectile_velocity,
                5,
                8,
                False,
                targeting_player=True,
                velocity_multiplier=50,
            ),
        )
        ent.Group(group)

    def destroy_entities(self) -> None:
        # check if enemies group exists
        if "enemies" not in self.pool.groups:
            return
        if len(self.pool.groups["enemies"]) > 0:
            entity = random.choice(self.pool.groups["enemies"])
            self.pool.remove_entity(entity)
