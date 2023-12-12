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
from components.audio import AudioComponent, AudioChannel

# misc
from misc.entity import EntityPool
from misc.logger import Logger
from misc.asset_store import AssetStore


class Spawner:
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger
        self.asset_store: AssetStore = game.asset_store
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
            Velocity(glm.vec2(-0.01, 0)),
            random_sprite,
            collider,
            health,
        )
        ent.Group("enemies")

    @staticmethod
    def random_angle(min, max):
        return glm.radians(random.uniform(min, max))

    def gen_explosion(self, x, y, size) -> None:
        """Generates an explosion at the given position with the given size"""
        particles = []
        colors = ["RED", "YELLOW", "ORANGE"]
        # play explosion sound
        audio = self.pool.create_entity(
            AudioComponent(
                channel=int(AudioChannel.EFFECT_CHANNEL.value),
                audio_id=self.asset_store.get_sound("explode"),
                loop=False,
            )
        )
        audio.Group("explosion audio")
        for i in range(0, size):
            speed = random.uniform(0.5, 10)
            angle = self.random_angle(0, 360)
            vel = glm.vec2(speed * glm.cos(angle), speed * glm.sin(angle))
            color = random.choice(colors)
            random_extra_age = random.randint(0, 25)
            age = 50.0 + random_extra_age
            part = self.pool.create_entity(
                Transform(glm.vec2(x, y), glm.vec2(1, 1), 0.0),
                Velocity(vel),
                Particle(age=age, max_age=age, color=Colors[color]),
            )
            part.Group("explosion particle")
            particles.append(part)

    def gen_sparks(self, x, y, size) -> None:
        """Generates sparks going the opposite direction of the entity being hit"""
        particles = []
        colors = ["RED", "YELLOW", "ORANGE"]

        audio = self.pool.create_entity(
            AudioComponent(
                channel=int(AudioChannel.EFFECT_CHANNEL.value),
                audio_id=self.asset_store.get_sound("hit"),
                loop=False,
            )
        )
        audio.Group("sparks audio")
        for i in range(0, size):
            speed = random.uniform(5, 10)
            angle = self.random_angle(180, 300)
            vel = glm.vec2(speed * glm.cos(angle), speed * glm.sin(angle))
            color = random.choice(colors)
            random_extra_age = random.randint(0, 40)
            age = 25.0 + random_extra_age
            part = self.pool.create_entity(
                Transform(glm.vec2(x, y), glm.vec2(1, 1), 0.0),
                Velocity(vel),
                Particle(age=age, max_age=age, color=Colors[color]),
            )
            part.Group("spark particle")
            particles.append(part)

    def destroy_entities(self) -> None:
        # check if enemies group exists
        if "enemies" not in self.pool.groups:
            return
        if len(self.pool.groups["enemies"]) > 0:
            entity = random.choice(self.pool.groups["enemies"])
            self.pool.remove_entity(entity)
