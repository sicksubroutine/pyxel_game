import esper as es


class EventHandler:
    def __init__(self, game):
        self.game = game

    def player_handlers(self):
        es.set_handler("shoot", self.game.projectile_system.player_shoot)
        es.set_handler("muzzle_flash", self.game.muzzle_flash_system.muzzle_flash)
        es.set_handler("collision", self.game.damage_system.on_collision)
        es.set_handler("explosion", self.game.spawner.gen_explosion)
        es.set_handler("sparks", self.game.spawner.gen_sparks)
        es.set_handler("player_death", self.game.player_system.player_death)

    def enable_event_handlers(self):
        es.set_handler("start_game", self.game.level_loader.next_level)
        es.set_handler("restart_game", self.game.restart_game)
        if self.game.level_loader.player_present:
            self.player_handlers()
