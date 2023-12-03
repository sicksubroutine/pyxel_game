from dataclasses import dataclass as component
from enum import Enum


class AudioChannel(Enum):
    BACKGROUND_CHANNEL = 0
    EFFECT_CHANNEL = 1
    UI_CHANNEL = 2
    PLAYER_CHANNEL = 3
    MUSIC_CHANNEL = 4


@component
class AudioComponent:
    audio_id: str = ""
    looping: bool = False
    is_playing: bool = False
    volume: float = 1.0
    start_time: float = 0.0
    delay: float = 0.0
    channel: AudioChannel = AudioChannel.BACKGROUND_CHANNEL
