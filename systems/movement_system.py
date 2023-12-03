import esper as es
from components.velocity import Velocity
from components.transform import Transform
import glm


class MovementSystem:
    def process(self, delta_time):
        for entity, (velocity, transform) in es.get_components(Velocity, Transform):
            transform.position += velocity.velocity
            velocity.velocity = glm.vec2(0, 0)
