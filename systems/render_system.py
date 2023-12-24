import esper as es
import pyxel as px
import heapq
from components.transform import Transform
from components.color import Colors
from components.sprite import Sprite
from misc.logger import Logger

from systems.player_system import PlayerSystem


class RenderSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.logger: Logger = game.logger

    def check_if_in_view(self, transform, sprite):
        if (
            transform.position.x < -sprite.width
            or transform.position.x > px.width
            or transform.position.y < -sprite.height
            or transform.position.y > px.height
        ):
            sprite.in_view = False
            return False
        else:
            sprite.in_view = True
            return True

    def convert_pal_to_color(self, color_name):
        try:
            if color_name not in Colors.__members__:
                raise ValueError(f"{color_name} is not a valid color")
            color = Colors[color_name].value
            for i in range(1, 16):
                px.pal(i, color)
        except ValueError as e:
            self.logger.Log(e)

    def process(self, player_system: PlayerSystem):
        priority_queue = []
        for ent, (transform, sprite) in es.get_components(Transform, Sprite):
            in_view = self.check_if_in_view(transform, sprite)
            if in_view:
                heapq.heappush(
                    priority_queue, (int(sprite.layer), ent, transform, sprite)
                )

        while priority_queue:
            _, ent, transform, sprite = heapq.heappop(priority_queue)

            player_entity_id = player_system.player.entity_id

            if sprite.in_view:
                if sprite.hit_flash > 0:
                    sprite.hit_flash -= 1
                    self.convert_pal_to_color("RED")
                if sprite.hit_flash % 8 == 0 and player_entity_id == ent:
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
                elif ent != player_entity_id:
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
                px.pal()


class RenderMuzzleFlashSystem:
    def __init__(self, game):
        self.muzzle_flash_size = 0.0
        self.game = game

    def render(self):
        if self.muzzle_flash_size > 0.0:
            px.circ(self.x, self.y, self.muzzle_flash_size, 9)
            px.circ(self.x, self.y, self.muzzle_flash_size - 2, 8)
            self.muzzle_flash_size -= 1.0 if not self.game.paused else 0.0

    def muzzle_flash(self, x, y, muzzle_flash_size):
        self.x = x
        self.y = y
        self.muzzle_flash_size = muzzle_flash_size
