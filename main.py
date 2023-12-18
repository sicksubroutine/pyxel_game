import pyxel as px
import esper as es
import time

from misc.entity import EntityPool
from misc.logger import Logger
from misc.spawner import Spawner
from misc.asset_store import AssetStore

from level_loader.level_loader import LevelLoader

# Systems
from systems.keyboard_system import KeyboardSystem
from systems.movement_system import MovementSystem
from systems.render_system import RenderSystem, RenderMuzzleFlashSystem
from systems.star_system import StarSystem
from systems.projectile_systems import ProjectileEmitterSystem, ProjectileLifetimeSystem
from systems.collider_system import ColliderSystem, CollisionRenderSystem
from systems.damage_system import DamageSystem
from systems.sound_system import SoundSystem
from systems.player_system import PlayerSystem
from systems.particle_system import ParticleSystem
from systems.health_system import HealthSystem


class Game:
    def __init__(self):
        self.logger: Logger = Logger(console_print=True)
        self.pool: EntityPool = EntityPool(self.logger)
        self.asset_store: AssetStore = AssetStore(self.logger)
        self.debug = False
        self.frames = 0
        self.fps = 0
        self.last_clock = 0
        self.res_width = 64
        self.res_height = 64
        px.init(self.res_width, self.res_height, title="Game", fps=60)
        px.mouse(False)
        self.on_init()

    def systems_import(self):
        self.spawner = Spawner(self)
        self.keyboard_system = KeyboardSystem(self)
        self.movement_system = MovementSystem(self)
        self.render_system = RenderSystem(self)
        self.star_system = StarSystem()
        self.projectile_system = ProjectileEmitterSystem(self)
        self.projectile_lifetime_system = ProjectileLifetimeSystem(self)
        self.collider_system = ColliderSystem(self)
        self.collision_render_system = CollisionRenderSystem()
        self.muzzle_flash_system = RenderMuzzleFlashSystem()
        self.damage_system = DamageSystem(self)
        self.sound_system = SoundSystem(self)
        self.player_system = PlayerSystem(self)
        self.particle_system = ParticleSystem(self)
        self.health_system = HealthSystem()

    def enable_event_handlers(self):
        es.set_handler("shoot", self.projectile_system.player_shoot)
        es.set_handler("muzzle_flash", self.muzzle_flash_system.muzzle_flash)
        es.set_handler("collision", self.damage_system.on_collision)
        es.set_handler("explosion", self.spawner.gen_explosion)
        es.set_handler("sparks", self.spawner.gen_sparks)
        # es.set_handler("player_death", self.damage_system.on_player_death)

    def on_init(self):
        self.systems_import()
        self.level_loader: LevelLoader = LevelLoader(self, 1)
        self.player = self.level_loader.player
        self.enable_event_handlers()

    def fps_counter(self):
        self.frames += 1
        new_now = int(time.time())
        if new_now != self.last_clock:
            self.fps = self.frames
            self.frames = 0
            self.last_clock = new_now

    def update(self):
        self.level_loader.spawn_schedule()
        self.star_system.update()
        self.collider_system.process()
        self.keyboard_system.process()
        self.movement_system.process()
        self.projectile_lifetime_system.process()
        self.sound_system.process()
        self.health_system.process()
        self.fps_counter()

    def render(self):
        px.cls(0)
        self.star_system.render()
        self.render_system.process()
        self.muzzle_flash_system.render()
        self.particle_system.process()
        if self.debug:
            self.collision_render_system.process()
            px.text(0, 0, f"FPS: {self.fps}", 7)
            px.text(0, 8, f"Entities: {len(self.pool.entities)}", 7)

    def run(self):
        px.run(self.update, self.render)


if __name__ == "__main__":
    game = Game()
    game.run()
