from components.animation import Animation, AniFrame
from components.sprite import Sprite, SpriteLayer
import esper as es
from misc.logger import Logger


class AnimationSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.logger: Logger = game.logger

    def process(self):
        for entity, (animation, sprite) in es.get_components(Animation, Sprite):
            sprite.u = animation.frames[animation.current_frame].u
            sprite.v = animation.frames[animation.current_frame].v
            sprite.img = animation.frames[animation.current_frame].img
            sprite.width = animation.frames[animation.current_frame].w
            sprite.height = animation.frames[animation.current_frame].h
