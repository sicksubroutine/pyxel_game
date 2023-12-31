import random
import glm

# components
from components.transform import Transform
from components.velocity import Velocity
from components.particle import Particle
from components.color import Colors
from components.audio import AudioComponent, AudioChannel
from components.animation import Animation, AniFrame

# misc
from misc.entity import EntityPool
from misc.logger import Logger
from misc.asset_store import AssetStore
from misc.utils import Utils


class Explosion:
    def __init__(self):
        self.components = [
            Animation(
                frames=[
                    AniFrame(u=40, v=32, w=16, h=16, img=2),
                    AniFrame(u=56, v=32, w=16, h=16, img=2),
                    AniFrame(u=72, v=32, w=16, h=16, img=2),
                    AniFrame(u=88, v=32, w=16, h=16, img=2),
                ],
                num_frames=4,
                frame_rate=0.1,
                looping=False,
            )
        ]


class Spawner:
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger
        self.asset_store: AssetStore = game.asset_store
        self.logger.Log("Spawner initialized")

    def gen_enemy(self, enemy_class) -> None:
        ent = self.pool.create_entity(*enemy_class.components)
        ent.Group("enemies")
        return ent

    def gen_explosion(self, x, y, size) -> None:
        """Generates an explosion at the given position with the given size"""
        particles = []
        colors = ["RED", "YELLOW", "ORANGE"]
        audio = self.pool.create_entity(
            AudioComponent(
                channel=int(AudioChannel.EFFECT_CHANNEL.value) + 1,
                audio_id=self.asset_store.get_sound("explode"),
                loop=False,
            )
        )
        audio.Group("explosion audio")
        for i in range(0, size):
            speed = random.uniform(0.5, 10)
            angle = Utils.random_angle(0, 360)
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
                channel=int(AudioChannel.EFFECT_CHANNEL.value) + 2,
                audio_id=self.asset_store.get_sound("hit"),
                loop=False,
            )
        )
        audio.Group("sparks audio")
        for i in range(0, size):
            speed = random.uniform(5, 10)
            angle = Utils.random_angle(180, 300)
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
        if "enemies" not in self.pool.groups:
            return
        if len(self.pool.groups["enemies"]) > 0:
            entity = random.choice(self.pool.groups["enemies"])
            self.pool.remove_entity(entity)
