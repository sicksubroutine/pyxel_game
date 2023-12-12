import esper as es
import random
import glm

# components
from components.transform import Transform
from components.velocity import Velocity
from components.sprite import Sprite, SpriteLayer
from components.collider import Collider
from components.health import Health
from components.particle import Particle
from components.color import Colors

# misc
from misc.entity import EntityPool
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
        # random_pos = glm.vec2(random.randint(0, 110), random.randint(0, 50))
        # random_vel = glm.vec2(random.randint(1, 2), random.randint(0, 0))
        random_sprite = random.choice(list(self.enemy_types.values()))
        width = random_sprite.width
        height = random_sprite.height
        health = Health(100, 100, False)
        collider = Collider(width, height, glm.vec2(0, 0), "enemies")
        ent = self.pool.create_entity(
            Transform(glm.vec2(32, 10), glm.vec2(4, 4), 0.0),
            Velocity(glm.vec2(-0.25, 0)),
            random_sprite,
            collider,
            health,
        )
        ent.Group("enemies")

    def gen_explosion(self, x, y, size) -> None:
        """Generates an explosion at the given position with the given size"""
        particles = []
        colors = ["RED", "YELLOW", "ORANGE"]
        for i in range(0, size):
            # random speed between 0.1 and 1
            speed = random.uniform(0.5, 5)
            angle = random.randint(0, 360)
            vel = glm.vec2(speed * glm.cos(angle), speed * glm.sin(angle))
            color = random.choice(colors)
            random_extra_age = random.randint(0, 45)
            age = 50.0 + random_extra_age
            part = self.pool.create_entity(
                Transform(glm.vec2(x, y), glm.vec2(1, 1), 0.0),
                Velocity(vel),
                Particle(age=age, max_age=age, color=Colors[color]),
            )
            particles.append(part)

    def destroy_entities(self) -> None:
        # check if enemies group exists
        if "enemies" not in self.pool.groups:
            return
        if len(self.pool.groups["enemies"]) > 0:
            entity = random.choice(self.pool.groups["enemies"])
            self.pool.remove_entity(entity)
