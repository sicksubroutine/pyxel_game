from dataclasses import dataclass as component
from enum import Enum
from components.base import BaseComponent


class Colors(Enum):
    def __int__(self) -> int:
        return int(self.value)

    BLACK = 0
    DARK_BLUE = 1
    VIOLET = 2
    GREEN = 3
    BROWN = 4
    DARK_BLUE_2 = 5
    LIGHT_BLUE = 6
    WHITE = 7
    RED = 8
    ORANGE = 9
    YELLOW = 10
    LIME_GREEN = 11
    LIGHT_BLUE_2 = 12
    GRAY = 13
    PEACH = 14
    KHAKI = 15


colors = {color: Colors[color].value for color in Colors.__members__}


@component
class Color(BaseComponent):
    color: Colors = Colors.BLACK
