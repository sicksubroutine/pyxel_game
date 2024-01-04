import esper as es


class EventHandler:
    def __init__(self, game):
        self.game = game

    def enable_event_handlers(self):
        es.set_handler("start_game", self.level_loader.next_level)
        es.set_handler("restart_game", self.restart_game)
        if self.game.level_loader.player_present:
            es.set_handler("shoot", self.projectile_system.player_shoot)
            es.set_handler("muzzle_flash", self.muzzle_flash_system.muzzle_flash)
            es.set_handler("collision", self.damage_system.on_collision)
            es.set_handler("explosion", self.spawner.gen_explosion)
            es.set_handler("sparks", self.spawner.gen_sparks)
            es.set_handler("player_death", self.player_system.player_death)
