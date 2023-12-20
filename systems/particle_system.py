import pyxel as px
import esper as es
import glm
from components.transform import Transform
from components.velocity import Velocity
from components.particle import Particle
from components.color import Colors
from misc.entity import EntityPool
from misc.logger import Logger

EPSILON = 0.000001
SLOWDOWN = 25


class ParticleSystem(es.Processor):
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger

    def process(self):
        for ent, (transform, velocity, particle) in es.get_components(
            Transform, Velocity, Particle
        ):
            vel = velocity.velocity if not self.game.paused else glm.vec2(0, 0)
            if particle.age > 0:
                particle.age -= 1 if not self.game.paused else 0
                # fade out over time
                vel -= (
                    (vel / (pow((particle.age) + EPSILON, 0.975))) * SLOWDOWN
                    if not self.game.paused
                    else 0
                )
                transform.position += vel
                # fade from white, to red, to yellow, to orange, to grey
                color = int(particle.color)
                if particle.age < 10:
                    color = int(Colors.GRAY)
                elif particle.age < particle.max_age / 2:
                    color = int(Colors.ORANGE)
                elif particle.age < particle.max_age / 1.5:
                    color = int(Colors.YELLOW)
                elif particle.age < particle.max_age / 1.25:
                    color = int(Colors.RED)
                elif particle.age > particle.max_age / 1.15:
                    color = int(Colors.WHITE)
                px.pset(transform.position.x, transform.position.y, color)
            else:
                self.pool.remove_entity(ent)
