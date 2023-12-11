from dataclasses import dataclass as component
from enum import Enum


class SoundTemplate:
    id_num = 0

    def __init__(self):
        ...


class Sound(SoundTemplate):
    def __init__(self):
        super().__init__()
        self.id = Sound.id_num
        Sound.id_num += 1

    def __str__(self) -> str:
        return str(self.id)

    def __int__(self) -> int:
        return self.id


class AudioChannel(Enum):
    EFFECT_CHANNEL = 0
    UI_CHANNEL = 1
    PLAYER_CHANNEL = 2
    MUSIC_CHANNEL = 3


@component
class AudioComponent:
    audio_id: str = ""
    loop: bool = False
    is_playing: bool = False
    start_time: float = 0.0
    delay: float = 0.0
    channel: AudioChannel = AudioChannel.EFFECT_CHANNEL
