from misc.entity import EntityPool, Entity
from misc.logger import Logger
from components.sprite import Sprite


class PlayerSystem:
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger
        self.player: Entity = None
        self.player_sprite: Sprite = None
        self.components = {}

    def player_setup(self, *components):
        self.components = {str(c): c for c in components}
        self.components["sprite"] = self.player_sprite
        components = list(self.components.values())
        self.player: Entity = self.pool.create_entity(*components)
        self.player.Group("player")
        return self.player

    def player_death(self):
        self.logger.Log("Player death")
        self.components = {}
        self.pool.remove_entity(self.player)
        self.player = None

    def respawn_player(self, *components):
        self.player = self.player_setup(*components)
