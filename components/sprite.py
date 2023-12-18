from enum import Enum
from dataclasses import dataclass as component
from components.base import BaseComponent


class SpriteLayer(Enum):
    """SpriteLayer enum for tracking sprite layers, used for rendering order"""

    def __int__(self) -> int:
        return int(self.value)

    BACKGROUND_LAYER = 0
    DECORATION_LAYER = 1
    ENEMY_LAYER = 2
    BULLET_LAYER = 3
    PLAYER_LAYER = 4
    GUI_LAYER = 5


@component
class Sprite(BaseComponent):
    """Sprite component for tracking sprite data for an entity"""

    width: int = 0
    height: int = 0
    img: int = 0
    u: int = 0
    v: int = 0
    default_u: int = u  # used for changing sprite depending on keyboard input
    layer: SpriteLayer = SpriteLayer.BACKGROUND_LAYER
    is_fixed: bool = False
    in_view: bool = False
    hit_flash: int = 0
