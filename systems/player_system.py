from misc.entity import EntityPool, Entity
from misc.logger import Logger
from components.sprite import Sprite
import glm


class PlayerSystem:
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger
        self.player: Entity = None
        self.player_sprite: Sprite = None
        self.player_position = None
        self.components = {}

    def get_player_position(self) -> glm.vec2:
        position = self.components["transform"].position
        x, y = position.x, position.y
        return glm.vec2(x, y)

    def player_setup(self, *components) -> Entity:
        if self.components:
            self.player_position = self.get_player_position()
        self.components = {str(c): c for c in components}
        self.components["sprite"] = self.player_sprite  # ship selection
        if not self.player_position is None:
            transform = self.components["transform"]
            transform.position = self.player_position
            self.components["transform"] = transform
        components = list(self.components.values())
        self.player: Entity = self.pool.create_entity(*components)
        self.player.Group("player")
        return self.player

    def player_death(self):
        self.logger.Log("Player death")
        self.pool.remove_entity(self.player.entity_id, True)
        self.components = {}
        self.player = None

    def respawn_player(self, *components):
        self.player = self.player_setup(*components)
