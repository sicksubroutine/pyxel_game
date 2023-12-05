import esper as es
import glm
import pyxel as px

from components.transform import Transform
from components.color import Color, Colors


class RenderSystem:
    def process(self):
        for ent, (transform, color) in es.get_components(Transform, Color):
            px.rect(
                transform.position.x,
                transform.position.y,
                transform.scale.x,
                transform.scale.y,
                color.color.value,
            )
