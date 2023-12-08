import esper as es
import pyxel as px
from components.transform import Transform
from components.collider import Collider


class ColliderSystem(es.Processor):
    # a method to check if two rectangles are colliding
    def is_colliding(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return x1 < x2 + w2 and x2 < x1 + w1 and y1 < y2 + h2 and y2 < y1 + h1

    def process(self):
        for ent, (transform, collider) in es.get_components(Transform, Collider):
            collider.is_colliding = False
            for ent2, (transform2, collider2) in es.get_components(Transform, Collider):
                if ent == ent2:
                    continue
                if collider.group == collider2.group:
                    continue
                if self.is_colliding(
                    transform.position.x,
                    transform.position.y,
                    collider.width,
                    collider.height,
                    transform2.position.x,
                    transform2.position.y,
                    collider2.width,
                    collider2.height,
                ):
                    collider.is_colliding = True
                    # TODO: Dispatch collision event


class CollisionRenderSystem(es.Processor):
    def process(self):
        for ent, (transform, collider) in es.get_components(Transform, Collider):
            if not collider.is_colliding:
                px.rectb(
                    transform.position.x,
                    transform.position.y,
                    collider.width,
                    collider.height,
                    7,
                )
            else:
                px.rectb(
                    transform.position.x,
                    transform.position.y,
                    collider.width,
                    collider.height,
                    8,
                )
