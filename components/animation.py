from dataclasses import dataclass as component
from components.base import BaseComponent


@component
class Animation(BaseComponent):
    """Animation component for animating sprites"""

    num_frames: int = 1
    current_frame: int = 0
    frame_rate: int = 0
    looping: bool = False
    start_time: float = 0.0
