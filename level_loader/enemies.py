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
        off_x: int,
        off_y: int,
        game,
        health,
    ):
        self.game = game
        self.spawner: Spawner = game.spawner
        self.logger: Logger = game.logger
        self.sprite = Sprite(w, h, img, u, v, layer, is_fixed)
        self.velocity = Velocity(glm.vec2(0.0, vel_y))
        self.transform = Transform(glm.vec2(x, y), glm.vec2(4, 4), 0)
        self.collider = Collider(w, h, glm.vec2(off_x, off_y), "enemies")
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
        self.entity = self.spawner.gen_enemy(self)

    def enemy_behavior(self):
        ...


class Boss1(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=16,
            h=16,
            img=0,
            u=32,
            v=64,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=750,
        )


class Boss2(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=16,
            h=16,
            img=0,
            u=48,
            v=64,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=800,
        )


class Boss3(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=16,
            h=16,
            img=0,
            u=32,
            v=48,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=1000,
        )


class Boss4(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=16,
            h=16,
            img=0,
            u=48,
            v=48,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=1500,
        )


class Boss5(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=16,
            h=16,
            img=0,
            u=64,
            v=48,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=1500,
        )


class Boss6(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=16,
            h=16,
            img=0,
            u=64,
            v=64,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=1500,
        )


class RedGuy(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=8,
            h=8,
            img=0,
            u=40,
            v=32,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=300,
        )


class RedGuy2(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=8,
            h=8,
            img=0,
            u=40,
            v=16,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=300,
        )


class RedGuy3(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=8,
            h=8,
            img=0,
            u=72,
            v=0,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=300,
        )


class GreenGuy(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=8,
            h=8,
            img=0,
            u=48,
            v=32,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=150,
        )


class GreenGuy2(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=8,
            h=8,
            img=0,
            u=56,
            v=32,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=300,
        )


class BlueGuy(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=8,
            h=8,
            img=0,
            u=32,
            v=16,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=0,
            off_y=0,
            game=game,
            health=300,
        )


class WhiteGuy(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=8,
            h=8,
            img=0,
            u=32,
            v=0,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=1,
            off_y=0,
            game=game,
            health=50,
        )


class OrangeGuy(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=8,
            h=8,
            img=0,
            u=48,
            v=40,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=1,
            off_y=0,
            game=game,
            health=100,
        )


class OrangeGuy2(Enemy):
    def __init__(self, game, x, y, vel_y):
        super().__init__(
            w=8,
            h=8,
            img=0,
            u=56,
            v=40,
            layer=SpriteLayer.ENEMY_LAYER,
            is_fixed=False,
            x=x,
            y=y,
            vel_x=0,
            vel_y=vel_y,
            off_x=1,
            off_y=0,
            game=game,
            health=100,
        )


class Enemies:
    def __init__(self, game):
        self.game = game
        self.enemies = []
        self.enemy_types = {
            "red_guy": RedGuy,
            "red_guy2": RedGuy2,
            "red_guy3": RedGuy3,
            "green_guy": GreenGuy,
            "green_guy2": GreenGuy2,
            "blue_guy": BlueGuy,
            "white_guy": WhiteGuy,
            "orange_guy": OrangeGuy,
            "orange_guy2": OrangeGuy2,
            "boss1": Boss1,
            "boss2": Boss2,
            "boss3": Boss3,
            "boss4": Boss4,
            "boss5": Boss5,
            "boss6": Boss6,
        }

    def get_enemy(self, name, x, y, vel_y) -> Enemy:
        enemy_class = self.enemy_types[name]
        enemy_instance = enemy_class(self.game, x, y, vel_y)
        self.enemies.append(enemy_instance)
        return enemy_instance

    def get_random_enemy(self, x, y) -> Enemy:
        enemy_class = random.choice(list(self.enemy_types.values()))
        enemy_instance = enemy_class(self.game, x, y)
        self.enemies.append(enemy_instance)
        return enemy_instance
