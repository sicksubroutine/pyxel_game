import glm
from dataclasses import dataclass as component


@component
class Transform:
    """Transform component for position, scale, and rotation"""

    position: glm.vec2 = glm.vec2(0, 0)
    scale: glm.vec2 = glm.vec2(1, 1)
    rotation: float = 0.0
