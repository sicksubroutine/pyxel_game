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
    def __int__(self) -> int:
        return int(self.value)

    EFFECT_CHANNEL = 0
    UI_CHANNEL = 1
    PLAYER_CHANNEL = 2
    MUSIC_CHANNEL = 3


@component
class AudioComponent:
    audio_id: int = -1
    loop: bool = False
    is_playing: bool = False
    delay: float = 0.0
    channel: AudioChannel = AudioChannel.EFFECT_CHANNEL
