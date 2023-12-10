import pyxel as px
import esper as es
import glm
import time as t

from misc.entity import Entity, EntityPool
from misc.logger import Logger
from misc.spawner import Spawner
from misc.asset_store import AssetStore

# Components
from components.transform import Transform
from components.velocity import Velocity
from components.keyboard_controller import KeyboardController
from components.collider import Collider
from components.color import Color, Colors
from components.sprite import Sprite, SpriteLayer
from components.projectile_emitter import ProjectileEmitter

# Systems
from systems.keyboard_system import KeyboardSystem
from systems.movement_system import MovementSystem
from systems.render_system import RenderSystem
from systems.star_system import StarSystem
from systems.projectile_systems import ProjectileEmitterSystem, ProjectileLifetimeSystem
from systems.collider_system import ColliderSystem, CollisionRenderSystem


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
        self.spawner = Spawner(self.pool, self.logger)
        self.keyboard_system = KeyboardSystem(self)
        self.movement_system = MovementSystem(self)
        self.render_system = RenderSystem()
        self.star_system = StarSystem()
        self.projectile_system = ProjectileEmitterSystem(self)
        self.projectile_lifetime_system = ProjectileLifetimeSystem(self)
        self.collider_system = ColliderSystem(self)
        self.collision_render_system = CollisionRenderSystem()

    def enable_event_handlers(self):
        es.set_handler("shoot", self.projectile_system.player_shoot)

    def on_init(self):
        self.asset_store.load_resource("sprites", "./assets/sprites.pyxres")

        self.systems_import()
        self.player_setup()
        self.enable_event_handlers()
        self.spawner.gen_random_entity()

    def player_setup(self):
        sprite = Sprite(8, 8, 0, 8, 32, SpriteLayer.PLAYER_LAYER, False, True)
        color = Color(color=Colors.RED)
        transform = Transform(
            position=glm.vec2(25, 25), scale=glm.vec2(5, 5), rotation=0.0
        )
        velocity = Velocity(velocity=glm.vec2(0, 0))
        keyboard = KeyboardController(
            glm.vec2(0, -1),
            glm.vec2(1, 0),
            glm.vec2(0, 1),
            glm.vec2(-1, 0),
        )
        collider = Collider(width=8, height=8, offset=glm.vec2(0, 0), group="player")
        proj_emitter = ProjectileEmitter(is_friendly=True)
        self.player: Entity = self.pool.create_entity(
            transform, velocity, keyboard, color, collider, sprite, proj_emitter
        )
        self.player.Group("player")

    def update(self):
        self.manual_fps_counter()
        self.star_system.update()
        self.collider_system.process()
        self.keyboard_system.process()
        self.movement_system.process()
        self.projectile_lifetime_system.process()

    def manual_fps_counter(self):
        self.frames += 1
        new_now = int(t.time())
        if new_now != self.last_clock:
            self.fps = self.frames
            self.frames = 0
            self.last_clock = new_now

    def render(self):
        px.cls(0)
        self.star_system.render()
        self.render_system.process()
        if self.debug:
            self.collision_render_system.process()
            px.text(0, 0, f"FPS: {self.fps}", 7)
            px.text(0, 8, f"Entities: {len(self.pool.entities)-1}", 7)

    def run(self):
        px.run(self.update, self.render)


if __name__ == "__main__":
    game = Game()
    game.run()
