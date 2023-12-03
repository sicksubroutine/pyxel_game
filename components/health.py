from dataclasses import dataclass as component


@component
class Health:
    """Component for tracking the health of an entity"""

    max_health: int
    current_health: int
    is_god_mode: bool = False
