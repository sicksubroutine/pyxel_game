import esper as es
from components.velocity import Velocity
from components.transform import Transform
import glm
from misc.entity import EntityPool, Entity


class MovementSystem:
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.width = game.res_width
        self.height = game.res_height

    def process(self):
        for entity, (velocity, transform) in es.get_components(Velocity, Transform):
            transform.position += velocity.velocity
            # get group
            enemy = self.pool.belongs_to_group(entity, "enemies")
            size_x = transform.scale.x
            size_y = transform.scale.y
            if transform.position.x > self.width - size_x:
                transform.position.x = self.width - size_x
                # bounce back
                if enemy:
                    velocity.velocity.x *= -1
            if transform.position.x < 0:
                transform.position.x = 0
                if enemy:
                    velocity.velocity.x *= -1

            if transform.position.y > self.height - size_y:
                transform.position.y = self.height - size_y
                # bounce back
                if enemy:
                    velocity.velocity.y *= -1
            if transform.position.y < 0:
                transform.position.y = 0
                if enemy:
                    velocity.velocity.y *= -1
