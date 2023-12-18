from dataclasses import dataclass as component
import glm
from components.base import BaseComponent


@component
class KeyboardController(BaseComponent):
    """KeyboardController component for tracking keyboard input"""

    up_velocity: glm.vec2 = glm.vec2(0)
    right_velocity: glm.vec2 = glm.vec2(0)
    down_velocity: glm.vec2 = glm.vec2(0)
    left_velocity: glm.vec2 = glm.vec2(0)
