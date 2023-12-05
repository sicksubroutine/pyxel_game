import esper as es
import random
import glm
from misc.entity import EntityPool
from components.transform import Transform
from components.velocity import Velocity
from components.color import Color, Colors
from misc.logger import Logger


class Spawner:
    def __init__(self, pool: EntityPool, logger: Logger):
        self.pool: EntityPool = pool
        self.logger: Logger = logger
        self.logger.Log("Spawner initialized")

    def gen_random_entity(self) -> None:
        random_pos = glm.vec2(random.randint(0, 110), random.randint(0, 110))

        random_vel = glm.vec2(random.randint(-1, 1), random.randint(-1, 1))
        random_color: Colors = random.choice(list(Colors))
        ent = self.pool.create_entity(
            Transform(random_pos, glm.vec2(4, 4), 0.0),
            Velocity(random_vel),
            Color(random_color),
        )
        ent.Group("enemies")

    def destroy_entities(self) -> None:
        # check if enemies group exists
        if "enemies" not in self.pool.groups:
            return
        if len(self.pool.groups["enemies"]) > 0:
            entity = random.choice(self.pool.groups["enemies"])
            self.pool.remove_entity(entity)
