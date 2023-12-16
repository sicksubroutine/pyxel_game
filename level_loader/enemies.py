from components.sprite import Sprite, SpriteLayer
from components.transform import Transform
from components.collider import Collider
from components.health import Health
from components.velocity import Velocity
from components.projectile_emitter import ProjectileEmitter
import glm
import random


class Enemy:
    def __init__(self, w, h, img, u, v, layer, is_fixed, x, y, vel_x, vel_y):
        self.sprite = Sprite(w, h, img, u, v, layer, is_fixed)
        self.velocity = Velocity(glm.vec2(vel_x, vel_y))
        self.transform = Transform(glm.vec2(x, y))
        self.collider = Collider(glm.vec2(w, h), glm.vec2(0, 0), "enemies")
        self.health = Health(100, 100, False)
        self.projectile_emitter = ProjectileEmitter(True, 10)


class Boss1(Enemy):
    def __init__(self):
        super().__init__(
            16, 16, 0, 32, 64, SpriteLayer.ENEMY_LAYER, False, 32, 10, -0.01, 0
        )


class Boss2(Enemy):
    def __init__(self):
        super().__init__(
            16, 16, 0, 48, 64, SpriteLayer.ENEMY_LAYER, False, 32, 10, -0.01, 0
        )


class Boss3(Enemy):
    def __init__(self):
        super().__init__(
            16, 16, 0, 32, 48, SpriteLayer.ENEMY_LAYER, False, 32, 10, -0.01, 0
        )


class Boss4(Enemy):
    def __init__(self):
        super().__init__(
            16, 16, 0, 48, 48, SpriteLayer.ENEMY_LAYER, False, 32, 10, -0.01, 0
        )


class Enemies:
    def __init__(self):
        self.enemy_types = {
            "boss1": Boss1,
            "boss2": Boss2,
            "boss3": Boss3,
            "boss4": Boss4,
        }

    def get_enemy(self, name):
        return self.enemy_types[name]()

    def get_random_enemy(self):
        return random.choice(list(self.enemy_types.values()))
