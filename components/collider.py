import glm
from dataclasses import dataclass as component


@component
class Collider:
    """Collider component for collision detection"""

    width: int = 0
    height: int = 0
    offset: glm.vec2 = glm.vec2(0)
    group: str = ""
    is_colliding: bool = False
