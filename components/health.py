from dataclasses import dataclass as component
from components.base import BaseComponent


@component
class Health(BaseComponent):
    """Component for tracking the health of an entity"""

    max_health: int
    current_health: int
    is_god_mode: bool = False
    hit_invuln: int = 0
