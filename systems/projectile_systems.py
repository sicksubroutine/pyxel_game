import esper as es
import glm
from misc.entity import EntityPool
from misc.logger import Logger
from misc.asset_store import AssetStore

# components
from components.transform import Transform
from components.sprite import Sprite, SpriteLayer
from components.projectile_emitter import ProjectileEmitter
from components.velocity import Velocity
from components.projectile import Projectile
from components.collider import Collider
from components.audio import AudioComponent, AudioChannel


class ProjectileEmitterSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger
        self.asset_store: AssetStore = game.asset_store

    def player_shoot(self):
        for ent, (transform, emitter) in es.get_components(
            Transform, ProjectileEmitter
        ):
            x = transform.position.x + 1
            y = transform.position.y + 1
            muzzle_flash = 6.0
            hit_damage = emitter.hit_damage
            es.dispatch_event("muzzle_flash", x + 2, y, muzzle_flash)
            self.create_projectile(x, y, emitter.is_friendly, hit_damage)

    def create_projectile(self, x, y, is_friendly, hit_damage, width=6, height=4):
        audio = AudioComponent(
            channel=int(AudioChannel.EFFECT_CHANNEL.value),
            audio_id=self.asset_store.get_sound("shoot"),
            loop=False,
        )
        transform = Transform(glm.vec2(x, y), glm.vec2(0.5, 0.5), 0.0)
        velocity = Velocity(velocity=glm.vec2(0, -1))
        sprite = Sprite(width, height, 1, 33, 9, SpriteLayer.BULLET_LAYER, False, True)
        collider = Collider(
            width=width, height=height, offset=glm.vec2(0, 0), group="bullet"
        )
        proj = Projectile(
            duration=100.0,
            hit_damage=hit_damage,
            is_friendly=is_friendly,
            start_time=0.0,
        )
        projectile = self.pool.create_entity(
            transform, sprite, collider, velocity, proj, audio
        )
        projectile.Group("bullet")

    def process(self):
        for ent, (transform, emitter, sprite) in es.get_components(
            Transform, ProjectileEmitter, Sprite
        ):
            # TODO: handle the shooting of enemies
            ...


class ProjectileLifetimeSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger
        self.timer = 0.0

    def process(self):
        self.timer += 1.0
        for ent, (transform, projectile) in es.get_components(Transform, Projectile):
            if projectile.start_time == 0.0:
                projectile.start_time = self.timer
            if (
                self.timer - projectile.start_time >= projectile.duration
                or transform.position.y < 0
            ):
                self.pool.remove_entity(ent)
