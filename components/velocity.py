import glm
from dataclasses import dataclass as component
from components.base import BaseComponent


@component
class Velocity(BaseComponent):
    """Velocity component for tracking velocity of an entity"""

    velocity: glm.vec2 = glm.vec2(0.0)
