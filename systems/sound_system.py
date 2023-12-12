import pyxel as px
import esper as es

from components.audio import AudioComponent
from misc.logger import Logger
from misc.entity import EntityPool


class SoundSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.logger: Logger = game.logger
        self.pool: EntityPool = game.pool

    def process(self):
        for ent, (audio) in es.get_component(AudioComponent):
            channel = int(audio.channel)
            if not audio.is_playing:
                px.play(ch=channel, snd=audio.audio_id, loop=audio.loop)
                audio.is_playing = True
            if px.play_pos(channel) is None and not audio.loop and audio.is_playing:
                es.remove_component(ent, AudioComponent)
                # need to check if the entity has zero components, if so, delete it
                if len(es.components_for_entity(ent)) == 0:
                    self.pool.remove_entity(ent)
