from dataclasses import dataclass as component
import glm


@component
class ProjectileEmitter:
    """ProjectileEmitter component for tracking projectile emitter attached to an entity"""

    fire_delay: float = 25
    repeat_frequency: float = 0
    projectile_velocity: glm.vec2 = glm.vec2(0)
    projectile_duration: float = 0
    hit_damage: int = 0
    is_friendly: bool = False
    targeting_player: bool = False
    velocity_multiplier: float = 1
    last_emission_time: float = 0.0
    audio_id: str = "shoot"
