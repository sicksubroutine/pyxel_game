import pyxel as px
import esper as es
import time

from misc.entity import EntityPool
from misc.logger import Logger
from misc.spawner import Spawner
from misc.asset_store import AssetStore
from misc.config import ConfigManager

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


class BootStrapper:
    """Responsible for initializing the game and restarting an instance if needed"""

    def __init__(self):
        self.config = ConfigManager()
        self.logger: Logger = Logger(
            console_print=True, file_write=True, file_path=self.config.log_file_name
        )
        self.logger.Log("BootStrapper initialized")

    def start_game(self):
        self.game: Game = Game(self, 0)
        self.game.run()

    def restart(self, current_level=0):
        self.logger.Log("Restarting game...")
        self.game: Game = Game(self, current_level)
        self.game.run()


class Game:
    def __init__(self, bootstrap, current_level=0):
        self.config = bootstrap.config
        self.logger: Logger = bootstrap.logger
        self.pool: EntityPool = EntityPool(self.logger)
        self.asset_store: AssetStore = AssetStore(self.logger)
        self.debug = self.config.debug
        self.frames = 0
        self.fps = self.config.target_fps
        self.last_clock = 0
        self.res_width = self.config.window_width
        self.res_height = self.config.window_height
        self.paused = False
        self.keypress_delay = 0.0
        px.init(
            self.res_width, self.res_height, title="Untitled 64x64 Shmup", fps=self.fps
        )
        self.systems_import(current_level)
        self.level_init()

    def systems_import(self, level):
        self.spawner = Spawner(self)
        self.keyboard_system = KeyboardSystem(self)
        self.movement_system = MovementSystem(self)
        self.render_system = RenderSystem(self)
        self.star_system = StarSystem()
        self.projectile_system = ProjectileEmitterSystem(self)
        self.projectile_lifetime_system = ProjectileLifetimeSystem(self)
        self.collider_system = ColliderSystem(self)
        self.collision_render_system = CollisionRenderSystem()
        self.muzzle_flash_system = RenderMuzzleFlashSystem(self)
        self.damage_system = DamageSystem(self)
        self.sound_system = SoundSystem(self)
        self.player_system = PlayerSystem(self)
        self.particle_system = ParticleSystem(self)
        self.level_loader: LevelLoader = LevelLoader(self, level)

    def enable_event_handlers(self):
        es.set_handler("start_game", self.level_loader.next_level)
        if self.level_loader.player_present:
            es.set_handler("shoot", self.projectile_system.player_shoot)
            es.set_handler("muzzle_flash", self.muzzle_flash_system.muzzle_flash)
            es.set_handler("collision", self.damage_system.on_collision)
            es.set_handler("explosion", self.spawner.gen_explosion)
            es.set_handler("sparks", self.spawner.gen_sparks)
            es.set_handler("player_death", self.player_system.player_death)

    def level_init(self):
        if self.level_loader.player_present:
            self.player = self.level_loader.player
        if self.level_loader.menu_present:
            self.menu_render = self.level_loader.menu_render
            self.menu_update = self.level_loader.menu_update
        self.enable_event_handlers()

    def fps_counter(self):
        self.frames += 1
        new_now = int(time.time())
        if new_now != self.last_clock:
            self.fps = self.frames
            self.frames = 0
            self.last_clock = new_now

    def update(self):
        self.keypress_delay -= 1.0 if self.keypress_delay > 0.0 else 0.0
        if not self.paused:
            self.level_loader.spawn_schedule()
            self.star_system.update()
            self.collider_system.process()
            self.keyboard_system.process()
            self.movement_system.process()
            self.projectile_lifetime_system.process()
            self.sound_system.process()
        if self.level_loader.menu_present:
            self.menu_update()
        self.fps_counter()

    def render(self):
        px.cls(0)
        self.star_system.render()
        self.render_system.process(self.player_system)
        self.muzzle_flash_system.render()
        self.particle_system.process()
        if self.level_loader.menu_present:
            self.menu_render()
        if self.debug:
            self.collision_render_system.process()
            px.text(0, 0, f"FPS: {self.fps}", 7)
            px.text(0, 8, f"Entities: {len(self.pool.entities)}", 7)

    def run(self):
        px.run(self.update, self.render)


if __name__ == "__main__":
    boot_strapper = BootStrapper()
    boot_strapper.start_game()
