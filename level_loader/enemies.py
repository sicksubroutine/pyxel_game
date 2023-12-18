from components.sprite import Sprite, SpriteLayer
from components.transform import Transform
from components.collider import Collider
from components.health import Health
from components.velocity import Velocity
from components.projectile_emitter import ProjectileEmitter
import glm
import random
from misc.spawner import Spawner
from misc.logger import Logger


class Enemy:
    def __init__(
        self,
        w: int,
        h: int,
        img: int,
        u: int,
        v: int,
        layer: SpriteLayer,
        is_fixed: bool,
        x: int,
        y: int,
        vel_x: int,
        vel_y: int,
        game,
        health,
    ):
        self.game = game
        self.spawner: Spawner = game.spawner
        self.logger: Logger = game.logger
        self.sprite = Sprite(w, h, img, u, v, layer, is_fixed)
        self.velocity = Velocity(glm.vec2(0.0, 0.25))
        self.transform = Transform(glm.vec2(x, y), glm.vec2(4, 4), 0)
        self.collider = Collider(w, h, glm.vec2(0, 0), "enemies")
        self.health = Health(health, health, False)
        # self.projectile_emitter = ProjectileEmitter(False, 10)
        self.group = "enemies"
        self.entity = None
        self.components = [
            self.sprite,
            self.velocity,
            self.transform,
            self.collider,
            self.health,
        ]
        self.on_init()

    def on_init(self):
        ...


class Boss1(Enemy):
    def __init__(self, x, y, game, health):
        super().__init__(
            16,
            16,
            0,
            32,
            64,
            SpriteLayer.ENEMY_LAYER,
            False,
            x,
            y,
            -0.01,
            0,
            game,
            health,
        )

    def on_init(self):
        self.entity = self.spawner.gen_enemy(self)


class Boss2(Enemy):
    def __init__(self, x, y, game, health):
        super().__init__(
            16,
            16,
            0,
            48,
            64,
            SpriteLayer.ENEMY_LAYER,
            False,
            x,
            y,
            -0.01,
            0,
            game,
            health,
        )

    def on_init(self):
        self.entity = self.spawner.gen_enemy(self)


class Boss3(Enemy):
    def __init__(self, x, y, game, health):
        super().__init__(
            16,
            16,
            0,
            32,
            48,
            SpriteLayer.ENEMY_LAYER,
            False,
            x,
            y,
            -0.01,
            0,
            game,
            health,
        )

    def on_init(self):
        self.entity = self.spawner.gen_enemy(self)


class Boss4(Enemy):
    def __init__(self, x, y, game, health):
        super().__init__(
            16,
            16,
            0,
            48,
            48,
            SpriteLayer.ENEMY_LAYER,
            False,
            x,
            y,
            -0.01,
            0,
            game,
            health,
        )

    def on_init(self):
        self.entity = self.spawner.gen_enemy(self)


class Enemies:
    def __init__(self, game):
        self.game = game
        self.enemies = []
        self.enemy_types = {
            "boss1": Boss1,
            "boss2": Boss2,
            "boss3": Boss3,
            "boss4": Boss4,
        }

    def get_enemy(self, name, x, y, health) -> Enemy:
        enemy_class = self.enemy_types[name]
        enemy_instance = enemy_class(x, y, self.game, health)
        self.enemies.append(enemy_instance)
        return enemy_instance

    def get_random_enemy(self, x, y) -> Enemy:
        enemy_class = random.choice(list(self.enemy_types.values()))
        enemy_instance = enemy_class(x, y, self.game)
        self.enemies.append(enemy_instance)
        return enemy_instance
