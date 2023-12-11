from dataclasses import dataclass as component


@component
class Particle:
    """A component that represents a particle."""

    age: float = 0.0
    size: float = 0.0
    color: int = 0
    speed: float = 0.0
    x: float = 0.0
    y: float = 0.0
    angle: float = 0.0
    sx: float = 0.0
    sy: float = 0.0
