import pyxel as px
from components.color import colors


NUM_STARS = 50
STAR_COLOR_WHITE = 7


class StarSystem:
    def __init__(self, color_mode=None):
        self.stars = []
        for _ in range(NUM_STARS):
            self.stars.append(
                (
                    px.rndi(0, px.width - 1),
                    px.rndi(0, px.height - 1),
                    px.rndf(0.25, 2.5),
                )
            )
        self.color_mode = color_mode

    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += speed
            if y >= px.height:
                y -= px.height
            self.stars[i] = (x, y, speed)

    def render(self):
        for x, y, speed in self.stars:
            px.pset(
                x,
                y,
                colors["WHITE"]
                if speed > 2.0
                else colors["LIGHT_BLUE"]
                if speed > 1.0
                else colors["GRAY"]
                if speed > 0.5
                else colors["DARK_BLUE"],
            )
