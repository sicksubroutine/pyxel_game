from misc.entity import EntityPool, Entity
from misc.logger import Logger


class PlayerSystem:
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger
        self.player: Entity = None
        self.components = {}

    def player_setup(self, *components):
        self.components = {str(c): c for c in components}
        self.logger.Log(self.components)
        transform = self.components["transform"]
        position = transform.position
        self.logger.Log(position)
        self.player: Entity = self.pool.create_entity(*components)
        self.player.Group("player")
        return self.player

    def player_death(self):
        self.components = {}
        self.pool.remove_entity(self.player)

    def respawn_player(self):
        # TODO: need to get the player components from level_loader/level class
        self.player = self.player_setup()
