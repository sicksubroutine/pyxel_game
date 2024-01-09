from dataclasses import dataclass as component
from dataclasses import field
from components.base import BaseComponent


@component
class AniFrame(BaseComponent):
    """Animation frame component for animating sprites"""

    u: int = 0
    v: int = 0
    w: int = 0
    h: int = 0
    img: int = 0


@component
class Animation(BaseComponent):
    """Animation component for animating sprites"""

    frames: list = field(default_factory=list)  # list of AniFrames
    num_frames: int = 1
    current_frame: int = 0
    frame_rate: int = 0
    looping: bool = False
    start_time: float = 0.0
