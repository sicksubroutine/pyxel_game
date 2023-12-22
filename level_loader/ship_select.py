from level_loader.base import BaseLevel
from systems.player_system import PlayerSystem
from misc.logger import Logger
from components.color import colors
from components.sprite import Sprite, SpriteLayer


class ShipSelect(BaseLevel):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.logger: Logger = game.logger
        self.level_loader = game.level_loader
        self.player_system: PlayerSystem = game.player_system
        self.level_name = "Ship Selection"
        self.menu = True
        self.player_sprite = Sprite(
            width=8,
            height=8,
            img=0,
            default_u=8,
            u=8,
            v=8,
            layer=SpriteLayer.PLAYER_LAYER,
            is_fixed=False,
        )

    """
    TODO:
    1. Need to have defined set of sprites for ships to choose from
    2. Need to have a way to choose them
    3. Need to pass that sprite to the level loader/player_system
    """

    def menu_update(self):
        self.logger.Log("Ship Selection, not ready yet... moving to level 1")
        self.level_loader.next_level()
        return

        # the player sprite that will be updated based on the ship selected and
        # sent to the player_system
        # self.player_sprite = Sprite()

    def menu_render(self):
        ...
