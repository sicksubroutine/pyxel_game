import esper as es
from components.keyboard_controller import KeyboardController
from components.velocity import Velocity
from components.transform import Transform
from components.sprite import Sprite
import pyxel as px
import glm
from misc.spawner import Spawner
from misc.entity import EntityPool
from misc.logger import Logger


class KeyboardSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.spawner: Spawner = game.spawner
        self.logger: Logger = self.game.logger
        self.pool: EntityPool = game.pool
        self.keypress_delay = 0.0

    def process(self):
        for entity, (keyboard, velocity, _, sprite) in es.get_components(
            KeyboardController,
            Velocity,
            Transform,
            Sprite,
        ):
            if self.keypress_delay > 0.0:
                self.keypress_delay -= 1
            velocity.velocity = glm.vec2(0, 0)
            sprite.u = sprite.default_u

            # if ctrl+d is pressed, toggle debug mode
            if px.btn(px.KEY_CTRL) and px.btnp(px.KEY_D):
                self.game.debug = not self.game.debug
                self.logger.Log(f"Debug mode: {self.game.debug}")
                return

            if px.btn(px.KEY_W) and px.btn(px.KEY_A):
                velocity.velocity = keyboard.up_velocity + keyboard.left_velocity
                sprite.u -= sprite.width
            elif px.btn(px.KEY_W) and px.btn(px.KEY_D):
                velocity.velocity = keyboard.up_velocity + keyboard.right_velocity
                sprite.u += sprite.width
            elif px.btn(px.KEY_S) and px.btn(px.KEY_A):
                velocity.velocity = keyboard.down_velocity + keyboard.left_velocity
                sprite.u -= sprite.width
            elif px.btn(px.KEY_S) and px.btn(px.KEY_D):
                velocity.velocity = keyboard.down_velocity + keyboard.right_velocity
                sprite.u += sprite.width
            elif px.btn(px.KEY_W):
                velocity.velocity = keyboard.up_velocity
            elif px.btn(px.KEY_S):
                velocity.velocity = keyboard.down_velocity
            elif px.btn(px.KEY_A):
                velocity.velocity = keyboard.left_velocity
                sprite.u -= sprite.width
            elif px.btn(px.KEY_D):
                velocity.velocity = keyboard.right_velocity
                sprite.u += sprite.width

            # if ctrl period is pressed, output a list of all entities to log
            if px.btn(px.KEY_CTRL) and px.btnp(px.KEY_PERIOD):
                self.logger.Log("Entity list:")
                entities = self.pool.get_list_of_entities()
                for entity in entities:
                    self.logger.Log(f"Entity: {entity}")

            if px.btn(px.KEY_SPACE) and self.keypress_delay <= 0.0:
                self.keypress_delay = 10.0
                es.dispatch_event("shoot")

                # if px.btn(px.KEY_X) and self.keypress_delay <= 0.0:
                # self.keypress_delay = 10.0
                # self.spawner.gen_enemy()
            if px.btn(px.KEY_Z):
                self.spawner.destroy_entities()

            if px.btnp(px.KEY_ESCAPE):
                px.quit()
