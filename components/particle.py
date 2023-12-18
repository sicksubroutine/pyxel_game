from dataclasses import dataclass as component
from components.base import BaseComponent


@component
class Particle(BaseComponent):
    """A component that represents a particle."""

    age: float = 0.0
    max_age: float = 0.0
    color: int = 0
