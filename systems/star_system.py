import pyxel as px
from components.color import colors


NUM_STARS = 50
STAR_COLOR_WHITE = 7


class StarSystem:
    def __init__(self, star_colors=None):
        self.stars = []
        for _ in range(NUM_STARS):
            self.stars.append(
                (
                    px.rndi(0, px.width - 1),
                    px.rndi(0, px.height - 1),
                    px.rndf(0.25, 2.5),
                )
            )
        self.star_colors = star_colors
        self.fast_stars = colors[self.star_colors["fast_stars"]]
        self.slow_stars = colors[self.star_colors["slow_stars"]]
        self.fastest_stars = colors[self.star_colors["fastest_stars"]]
        self.slowest_stars = colors[self.star_colors["slowest_stars"]]

    def set_star_colors(self, star_colors):
        self.star_colors = star_colors
        self.fast_stars = colors[self.star_colors["fast_stars"]]
        self.slow_stars = colors[self.star_colors["slow_stars"]]
        self.fastest_stars = colors[self.star_colors["fastest_stars"]]
        self.slowest_stars = colors[self.star_colors["slowest_stars"]]

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
                self.fastest_stars
                if speed > 2.0
                else self.fast_stars
                if speed > 1.0
                else self.slow_stars
                if speed > 0.5
                else self.slowest_stars,
            )
