from dataclasses import dataclass as component
from components.base import BaseComponent


@component
class Projectile(BaseComponent):
    """Projectile component for tracking projectile data"""

    duration: float = 0
    hit_damage: int = 0
    is_friendly: bool = False
    start_time: float = 0.0
