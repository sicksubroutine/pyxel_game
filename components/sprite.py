from enum import Enum


class SpriteLayer(Enum):
    """SpriteLayer enum for tracking sprite layers, used for rendering"""

    BACKGROUND_LAYER = 0
    DECORATION_LAYER = 1
    GROUND_LAYER = 2
    AIR_LAYER = 3
    BULLET_LAYER = 4
    PLAYER_LAYER = 5
    GUI_LAYER = 6


class Sprite:
    """Sprite component for tracking sprite data for an entity"""

    def __init__(
        self, asset_id, width, height, layer, is_fixed, src_rect, in_view=False
    ):
        self.asset_id = asset_id
        self.width = width
        self.height = height
        self.layer = layer
        self.is_fixed = is_fixed
        self.src_rect: tuple = src_rect
        self.in_view = in_view
