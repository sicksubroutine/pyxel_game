from components.animation import Animation, AniFrame
from components.sprite import Sprite, SpriteLayer
import esper as es


class AnimationSystem(es.Processor):
    def __init__(self):
        self.frame_timer = 0.0

    def process(self):
        for entity, (animation, sprite) in es.get_components(Animation, Sprite):
            if animation.frame_timer >= animation.frame_rate:
                animation.frame_timer = 0.0
                animation.current_frame += 1
                if animation.current_frame >= animation.num_frames:
                    if animation.looping:
                        animation.current_frame = 0
                    else:
                        animation.current_frame = animation.num_frames - 1
                        animation.is_playing = False
                sprite.u = animation.frames[animation.current_frame].u
                sprite.v = animation.frames[animation.current_frame].v
                sprite.img = animation.frames[animation.current_frame].img
                sprite.width = animation.frames[animation.current_frame].w
                sprite.height = animation.frames[animation.current_frame].h
