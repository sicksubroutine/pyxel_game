import esper as es
from components.keyboard_controller import KeyboardController
from components.velocity import Velocity
from components.transform import Transform
import pyxel as px


class KeyboardSystem:
    def process(self, delta_time):
        for entity, (keyboard, velocity, transform) in es.get_components(
            KeyboardController, Velocity, Transform
        ):
            if px.btn(px.KEY_W):
                velocity.velocity = keyboard.up_velocity
            if px.btn(px.KEY_S):
                velocity.velocity = keyboard.down_velocity
            if px.btn(px.KEY_A):
                velocity.velocity = keyboard.left_velocity
            if px.btn(px.KEY_D):
                velocity.velocity = keyboard.right_velocity

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
