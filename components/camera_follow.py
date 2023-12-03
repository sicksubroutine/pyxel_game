from dataclasses import dataclass as component


@component
class Camera:
    """Camera class for tracking the camera position and size"""

    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0


@component
class CameraFollow:
    """CameraFollow component for following an entity(probably the player)"""

    follow: bool = True
