import glm
from dataclasses import dataclass as component


@component
class Velocity:
    """Velocity component for tracking velocity of an entity"""

    velocity: glm.vec2 = glm.vec2(0.0)
