import esper as es
from components.keyboard_controller import KeyboardController
from components.velocity import Velocity
from components.transform import Transform
from components.sprite import Sprite
import pyxel as px
from misc.spawner import Spawner
import glm


class KeyboardSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.spawner: Spawner = game.spawner

    def process(self):
        for entity, (keyboard, velocity, transform, sprite) in es.get_components(
            KeyboardController,
            Velocity,
            Transform,
            Sprite,
        ):
            velocity.velocity = glm.vec2(0, 0)
            sprite.u = sprite.default_u
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

            if px.btn(px.KEY_X):
                self.spawner.gen_random_entity()
            if px.btn(px.KEY_Z):
                self.spawner.destroy_entities()

            if px.btnp(px.KEY_ESCAPE):
                px.quit()
