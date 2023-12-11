# TODO: A sound system using Pxyel's sound system
import pyxel as px
import esper as es

from components.audio import AudioComponent


class SoundSystem(es.Processor):
    def process(self):
        for ent, (audio) in es.get_component(AudioComponent):
            if not audio.is_playing:
                px.play(ch=audio.channel.value, snd=audio.audio_id, loop=audio.loop)
                audio.is_playing = True
            if (
                px.play_pos(audio.channel.value) is None
                and not audio.loop
                and audio.is_playing
            ):
                es.remove_component(ent, AudioComponent)
