import esper as es
from components.keyboard_controller import KeyboardController
from components.velocity import Velocity
from components.transform import Transform
import pyxel as px
from misc.spawner import Spawner
import glm


class KeyboardSystem:
    def __init__(self, game):
        self.game = game
        self.spawner: Spawner = game.spawner

    def process(self):
        for entity, (keyboard, velocity, transform) in es.get_components(
            KeyboardController, Velocity, Transform
        ):
            velocity.velocity = glm.vec2(0, 0)
            if px.btn(px.KEY_W):
                velocity.velocity = keyboard.up_velocity
            if px.btn(px.KEY_S):
                velocity.velocity = keyboard.down_velocity
            if px.btn(px.KEY_A):
                velocity.velocity = keyboard.left_velocity
            if px.btn(px.KEY_D):
                velocity.velocity = keyboard.right_velocity
            if px.btn(px.KEY_X):
                self.spawner.gen_random_entity()
            if px.btn(px.KEY_Z):
                self.spawner.destroy_entities()

            # account for diagonal movement
            if px.btn(px.KEY_W) and px.btn(px.KEY_A):
                velocity.velocity = keyboard.up_velocity + keyboard.left_velocity
            if px.btn(px.KEY_W) and px.btn(px.KEY_D):
                velocity.velocity = keyboard.up_velocity + keyboard.right_velocity
            if px.btn(px.KEY_S) and px.btn(px.KEY_A):
                velocity.velocity = keyboard.down_velocity + keyboard.left_velocity
            if px.btn(px.KEY_S) and px.btn(px.KEY_D):
                velocity.velocity = keyboard.down_velocity + keyboard.right_velocity

            if px.btnp(px.KEY_ESCAPE):
                px.quit()
