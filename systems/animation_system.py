from components.animation import Animation
from components.sprite import Sprite
import esper as es
from misc.logger import Logger
from misc.entity import EntityPool
import sys

EPSILON = sys.float_info.epsilon


class AnimationSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.logger: Logger = game.logger
        self.pool: EntityPool = game.pool
        self.frame_timers = {}

    def process(self, delta_time):
        for entity, (animation, sprite) in es.get_components(Animation, Sprite):
            if entity not in self.frame_timers:
                self.frame_timers[entity] = 0.0

            self.frame_timers[entity] += delta_time
            frame_duration = (
                1.0 / (animation.frame_rate + EPSILON)
                if animation.frame_rate > 0
                else 0.0
            )

            if self.frame_timers[entity] >= frame_duration:
                self.frame_timers[entity] = 0.0
                animation.current_frame += 1
                if (
                    animation.current_frame >= animation.num_frames
                    and animation.looping
                ):
                    animation.current_frame = 0
                elif (
                    animation.current_frame >= animation.num_frames
                    and not animation.looping
                ):
                    self.pool.remove_entity(entity)
                    del self.frame_timers[entity]
                    continue

            sprite.u = animation.frames[animation.current_frame].u
            sprite.v = animation.frames[animation.current_frame].v
            sprite.img = animation.frames[animation.current_frame].img
            sprite.width = animation.frames[animation.current_frame].w
            sprite.height = animation.frames[animation.current_frame].h
