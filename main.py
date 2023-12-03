import pyxel as px
import esper as es
import glm
import time as t

from misc.entity import Entity, EntityPool
from misc.logger import Logger

# Components
from components.transform import Transform
from components.velocity import Velocity
from components.keyboard_controller import KeyboardController

# Systems
from systems.keyboard_system import KeyboardSystem
from systems.movement_system import MovementSystem


class Game:
    def __init__(self):
        self.logger: Logger = Logger(console_print=True)
        self.pool: EntityPool = EntityPool(self.logger)
        self.delta_time: float = 0.0
        self.frames = 0
        self.fps = 0
        self.last_clock = 0
        px.init(128, 128, title="Game", fps=60)
        self.on_init()

    def systems_import(self):
        self.keyboard_system = KeyboardSystem()
        self.movement_system = MovementSystem()

    def on_init(self):
        self.systems_import()
        transform = Transform(
            position=glm.vec2(25, 25), scale=glm.vec2(1, 1), rotation=0.0
        )
        velocity = Velocity(velocity=glm.vec2(0, 0))
        keyboard = KeyboardController(
            glm.vec2(0, -1),
            glm.vec2(1, 0),
            glm.vec2(0, 1),
            glm.vec2(-1, 0),
        )
        self.player: Entity = self.pool.create_entity(transform, velocity, keyboard)

    def update(self):
        self.manual_fps_counter()
        self.keyboard_system.process(self.delta_time)
        self.movement_system.process(self.delta_time)

    def manual_fps_counter(self):
        self.frames += 1
        new_now = int(t.time())
        if new_now != self.last_clock:
            self.fps = self.frames
            self.frames = 0
            self.last_clock = new_now

    def render(self):
        start = t.time()
        position = es.component_for_entity(self.player, Transform).position
        px.cls(0)
        px.rect(
            position.x,
            position.y,
            10,
            10,
            9,
        )
        # px.text(0, 0, f"FPS: {self.fps}", 7)
        # px.text(0, 10, f"Delta Time: {self.delta_time}", 7)
        self.delta_time = t.time() - start

    def run(self):
        px.run(self.update, self.render)


if __name__ == "__main__":
    game = Game()
    game.run()
