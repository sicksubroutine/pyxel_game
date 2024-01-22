from components.animation import Animation, AniFrame
from components.sprite import Sprite, SpriteLayer
import esper as es
from misc.logger import Logger


class AnimationSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.logger: Logger = game.logger
        self.timer = 0.0

    def process(self):
        self.timer += 1.0
        for entity, (animation, sprite) in es.get_components(Animation, Sprite):
            if animation.looping:
                if self.timer > animation.frame_rate:
                    animation.current_frame += 1
            else:
                if self.timer > animation.frame_rate:
                    animation.current_frame += 1
                    if animation.current_frame == animation.num_frames:
                        animation.current_frame = animation.num_frames - 1

            sprite.u = animation.frames[animation.current_frame].u
            sprite.v = animation.frames[animation.current_frame].v
            sprite.img = animation.frames[animation.current_frame].img
            sprite.width = animation.frames[animation.current_frame].w
            sprite.height = animation.frames[animation.current_frame].h
