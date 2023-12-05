import pyxel as px

NUM_STARS = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5


class StarSystem:
    def __init__(self):
        self.stars = []
        for i in range(NUM_STARS):
            self.stars.append(
                (
                    px.rndi(0, px.width - 1),
                    px.rndi(0, px.height - 1),
                    px.rndf(1, 2.5),
                )
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += speed
            if y >= px.height:
                y -= px.height
            self.stars[i] = (x, y, speed)

    def render(self):
        for x, y, speed in self.stars:
            px.pset(x, y, STAR_COLOR_HIGH if speed > 1.5 else STAR_COLOR_LOW)
