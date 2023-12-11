from enum import Enum


class SpriteLayer(Enum):
    """SpriteLayer enum for tracking sprite layers, used for rendering"""

    BACKGROUND_LAYER = 0
    DECORATION_LAYER = 1
    ENEMY_LAYER = 2
    BULLET_LAYER = 3
    PLAYER_LAYER = 4
    GUI_LAYER = 5


class Sprite:
    """Sprite component for tracking sprite data for an entity"""

    def __init__(self, width, height, img, u, v, layer, is_fixed, in_view=False):
        self.width = width
        self.height = height
        self.img = img
        self.u = u
        self.v = v
        self.default_u = u
        self.layer: SpriteLayer = layer
        self.is_fixed: bool = is_fixed
        self.in_view: bool = in_view
        self.hit_flash: int = 0
