import esper as es
from components.velocity import Velocity
from components.transform import Transform
import glm
from misc.entity import EntityPool, Entity


class MovementSystem:
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool

    def process(self):
        for entity, (velocity, transform) in es.get_components(Velocity, Transform):
            transform.position += velocity.velocity
            # get group
            player = self.pool.belongs_to_group(entity, "player")
            size_x = transform.scale.x
            size_y = transform.scale.y
            if transform.position.x > 128 - size_x:
                transform.position.x = 128 - size_x
                # bounce back
                if not player:
                    velocity.velocity.x *= -1
            if transform.position.x < 0:
                transform.position.x = 0
                if not player:
                    velocity.velocity.x *= -1

            if transform.position.y > 128 - size_y:
                transform.position.y = 128 - size_y
                # bounce back
                if not player:
                    velocity.velocity.y *= -1
            if transform.position.y < 0:
                transform.position.y = 0
                if not player:
                    velocity.velocity.y *= -1
