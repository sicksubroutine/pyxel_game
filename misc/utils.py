from glm import lerp, radians
from random import uniform


class Utils:
    @staticmethod
    def inv_lerp(a, b, v) -> float:
        return (v - a) / (b - a)

    @staticmethod
    def remap(a, b, c, d, v) -> float:
        t = Utils.inv_lerp(a, b, v)
        return lerp(c, d, t)

    @staticmethod
    def random_angle(min, max):
        return radians(uniform(min, max))
