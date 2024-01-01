import esper as es
import pyxel as px
from components.transform import Transform
from components.collider import Collider
from components.projectile import Projectile
from misc.entity import EntityPool
from misc.logger import Logger


class ColliderSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger

    def is_colliding(self, t1, col1, t2, col2):
        x1, y1 = t1.position.x, t1.position.y
        w1, h1 = col1.width, col1.height
        x2, y2 = t2.position.x, t2.position.y
        w2, h2 = col2.width, col2.height
        off_x1, off_y1 = col1.offset.x, col1.offset.y
        off_x2, off_y2 = col2.offset.x, col2.offset.y
        return (
            x1 + off_x1 < x2 + off_x2 + w2
            and x1 + off_x1 + w1 > x2 + off_x2
            and y1 + off_y1 < y2 + off_y2 + h2
            and y1 + off_y1 + h1 > y2 + off_y2
        )

    def process(self):
        for ent1, (transform, collider) in es.get_components(Transform, Collider):
            collider.is_colliding = False
            for ent2, (transform2, collider2) in es.get_components(Transform, Collider):
                if ent1 == ent2:
                    continue
                if collider.group == collider2.group:
                    continue

                if self.is_colliding(transform, collider, transform2, collider2):
                    if collider.group == "bullet" and collider2.group == "player":
                        if ent1 not in self.pool.entities:
                            continue
                        proj_emitter = self.pool.entity_get_component(ent1, Projectile)
                        if proj_emitter and proj_emitter.is_friendly:
                            continue
                    if collider2.group == "bullet" and collider.group == "player":
                        if ent2 not in self.pool.entities:
                            continue
                        proj_emitter = self.pool.entity_get_component(ent2, Projectile)
                        if proj_emitter and proj_emitter.is_friendly:
                            continue
                    collider.is_colliding = True
                    entity1 = {
                        "entity": ent1,
                        "group": collider.group,
                    }
                    entity2 = {
                        "entity": ent2,
                        "group": collider2.group,
                    }
                    es.dispatch_event("collision", entity1, entity2)


class CollisionRenderSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.pool = game.pool

    def process(self):
        if self.game.debug:
            # px.text(0, 0, f"FPS: {self.fps}", 7)
            px.text(0, 0, f"Delay: {self.game.level_loader.delay}", 7)
            px.text(0, 8, f"Entities: {len(self.pool.entities)}", 7)
            px.text(
                0, 16, f"Level: {self.game.level_loader.loaded_level.level_name}", 7
            )
            for ent, (transform, collider) in es.get_components(Transform, Collider):
                # White rectangle if not colliding, red if colliding while in debug mode
                if not collider.is_colliding:
                    px.rectb(
                        transform.position.x + collider.offset.x,
                        transform.position.y + collider.offset.y,
                        collider.width,
                        collider.height,
                        7,
                    )
                else:
                    px.rectb(
                        transform.position.x + collider.offset.x,
                        transform.position.y + collider.offset.y,
                        collider.width,
                        collider.height,
                        8,
                    )
