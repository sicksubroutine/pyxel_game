import esper as es
import random
import glm
from misc.entity import EntityPool
from components.transform import Transform
from components.velocity import Velocity
from components.sprite import Sprite, SpriteLayer
from components.collider import Collider
from components.health import Health
from misc.logger import Logger


class Spawner:
    def __init__(self, pool: EntityPool, logger: Logger):
        self.pool: EntityPool = pool
        self.logger: Logger = logger
        self.logger.Log("Spawner initialized")
        self.enemy_types = {
            "boss": Sprite(16, 16, 0, 32, 64, SpriteLayer.ENEMY_LAYER, False, True),
            "boss2": Sprite(16, 16, 0, 48, 64, SpriteLayer.ENEMY_LAYER, False, True),
            "boss3": Sprite(16, 16, 0, 32, 48, SpriteLayer.ENEMY_LAYER, False, True),
            "boss4": Sprite(16, 16, 0, 48, 48, SpriteLayer.ENEMY_LAYER, False, True),
        }

    def gen_random_entity(self) -> None:
        random_pos = glm.vec2(random.randint(0, 110), random.randint(0, 110))
        random_vel = glm.vec2(random.randint(-1, 1), random.randint(-1, 1))
        random_sprite = random.choice(list(self.enemy_types.values()))
        width = random_sprite.width
        height = random_sprite.height
        health = Health(100, 100, False)
        collider = Collider(width, height, glm.vec2(0, 0), "enemies")
        ent = self.pool.create_entity(
            Transform(random_pos, glm.vec2(4, 4), 0.0),
            Velocity(random_vel),
            random_sprite,
            collider,
            health,
        )
        ent.Group("enemies")

    def destroy_entities(self) -> None:
        # check if enemies group exists
        if "enemies" not in self.pool.groups:
            return
        if len(self.pool.groups["enemies"]) > 0:
            entity = random.choice(self.pool.groups["enemies"])
            self.pool.remove_entity(entity)
