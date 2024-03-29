import pyxel as px
import esper as es
import time
import sys

# helpers
from misc.entity import EntityPool
from misc.logger import Logger
from misc.spawner import Spawner
from misc.asset_store import AssetStore
from misc.config import ConfigManager
from misc.events import EventHandler
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
from systems.animation_system import AnimationSystem


EPSILON = sys.float_info.epsilon


class BootStrapper:
    """Responsible for initializing the game and restarting an instance if needed"""

    def __init__(self):
        self.config = ConfigManager()
        self.logger: Logger = Logger(
            console_print=self.config.debug_to_console,
            file_write=self.config.debug_to_file,
            file_path=self.config.log_file_name,
        )
        self.logger.Log("BootStrapper initialized")

    def start_game(self):
        self.game: Game = Game(self, "Start Menu")
        self.game.run()


class Game:
    def __init__(self, bootstrap, current_level="Start Menu"):
        self.boot_strapper: BootStrapper = bootstrap
        self.config = bootstrap.config
        self.logger: Logger = bootstrap.logger
        self.pool: EntityPool = EntityPool(self)
        self.asset_store: AssetStore = AssetStore(self)
        self.debug = self.config.debug
        self.frames = 0
        self.fps = self.config.target_fps
        self.delta_time = 0.0
        self.last_clock = 0
        self.res_width = self.config.window_width
        self.res_height = self.config.window_height
        self.paused = False
        self.keypress_delay = 0.0
        px.init(self.res_width, self.res_height, title=self.config.title, fps=self.fps)

        self.systems_import()
        self.event_handler = EventHandler(self)
        self.level_init(current_level)

    def systems_import(self):
        self.spawner = Spawner(self)
        self.keyboard_system = KeyboardSystem(self)
        self.movement_system = MovementSystem(self)
        self.render_system = RenderSystem(self)
        self.projectile_system = ProjectileEmitterSystem(self)
        self.projectile_lifetime_system = ProjectileLifetimeSystem(self)
        self.collider_system = ColliderSystem(self)
        self.collision_render_system = CollisionRenderSystem(self)
        self.muzzle_flash_system = RenderMuzzleFlashSystem(self)
        self.damage_system = DamageSystem(self)
        self.sound_system = SoundSystem(self)
        self.player_system = PlayerSystem(self)
        self.particle_system = ParticleSystem(self)
        self.animation_system = AnimationSystem(self)

    def level_init(self, level):
        self.level_loader: LevelLoader = LevelLoader(self, level)
        if self.level_loader.star_colors_present:
            star_colors = self.level_loader.star_colors
        if hasattr(self, "star_system"):
            self.star_system.set_star_colors(star_colors)
        else:
            self.star_system = StarSystem(star_colors)
        if self.level_loader.player_present:
            self.player = self.level_loader.player
        if self.level_loader.menu_present:
            self.menu_render = self.level_loader.menu_render
            self.menu_update = self.level_loader.menu_update
        self.event_handler.enable_event_handlers()

    def fps_counter(self):
        self.frames += 1
        new_now = time.perf_counter()
        if new_now - self.last_clock >= 1.0:
            self.fps = round(self.frames / (new_now - self.last_clock), 2)
            self.frames = 0
            self.last_clock = new_now
        self.delta_time = 1.0 / (self.fps + EPSILON)

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
            self.animation_system.process(self.delta_time)
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
        self.collision_render_system.process()

    def restart_game(self):
        self.pool.clear_all_entities()
        es.switch_world("empty")
        worlds = es.list_worlds()
        for world in worlds:
            if world != "empty":
                es.delete_world(world)
        self.level_init(self.level_loader.current_level)
        self.paused = False
        self.level_loader.loaded_level.menu_showing = False

    def run(self):
        px.run(self.update, self.render)


if __name__ == "__main__":
    boot_strapper = BootStrapper()
    boot_strapper.start_game()
