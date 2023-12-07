import esper as es
import glm
import pyxel as px
import heapq
from components.transform import Transform
from components.color import Color
from components.sprite import Sprite, SpriteLayer


class RenderSystem(es.Processor):
    def process(self):
        priority_queue = []
        for ent, (transform, sprite) in es.get_components(Transform, Sprite):
            heapq.heappush(priority_queue, (sprite.layer.value, ent, transform, sprite))

        while priority_queue:
            _, ent, transform, sprite = heapq.heappop(priority_queue)
            if sprite.in_view:
                px.blt(
                    transform.position.x,
                    transform.position.y,
                    sprite.img,
                    sprite.u,
                    sprite.v,
                    sprite.width,
                    sprite.height,
                    0,
                )
