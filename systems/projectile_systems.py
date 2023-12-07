import esper as es

from misc.entity import EntityPool
from misc.logger import Logger

from components.transform import Transform
from components.sprite import Sprite
from components.projectile_emitter import ProjectileEmitter


class ProjectileEmitterSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger

    def create_projectile(self):
        ...

    def process(self):
        for ent, (transform, emitter, sprite) in es.get_components(
            Transform, ProjectileEmitter, Sprite
        ):
            ...
