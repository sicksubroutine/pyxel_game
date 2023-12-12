from dataclasses import dataclass as component


@component
class Particle:
    """A component that represents a particle."""

    age: float = 0.0
    max_age: float = 0.0
    color: int = 0
