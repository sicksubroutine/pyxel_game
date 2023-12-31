import esper as es
from components.velocity import Velocity
from components.transform import Transform
from components.sprite import Sprite
from misc.entity import EntityPool


class MovementSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.width = game.res_width
        self.height = game.res_height

    def process(self):
        for entity, (velocity, transform, sprite) in es.get_components(
            Velocity, Transform, Sprite
        ):
            transform.position += velocity.velocity
            # get group
            enemy = self.pool.belongs_to_group(entity, "enemies")
            bullet = self.pool.belongs_to_group(entity, "bullet")
            if bullet:
                continue

            size_x = sprite.width
            size_y = sprite.height

            if enemy:
                velocity.velocity.y *= 1
                if transform.position.y > self.height + size_y:
                    self.pool.remove_entity(entity)

            # player movement
            if transform.position.x > self.width - size_x:
                transform.position.x = self.width - size_x

            if transform.position.x < 0:
                transform.position.x = 0

            if transform.position.y > self.height - size_y and not enemy:
                transform.position.y = self.height - size_y

            if transform.position.y < 0 and not enemy:
                transform.position.y = 0
