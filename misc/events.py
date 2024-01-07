import esper as es
from level_loader.level_loader import LevelLoader


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

    def general_game_handlers(self):
        es.set_handler("enable_pause", self.enable_pause)
        es.set_handler("disable_pause", self.disable_pause)
        # es.set_handler("toggle_fullscreen", self.game.toggle_fullscreen)
        es.set_handler("start_game", self.game.level_loader.next_level)
        es.set_handler("restart_game", self.game.restart_game)

    def enable_event_handlers(self):
        self.general_game_handlers()
        if self.game.level_loader.player_present:
            self.player_handlers()

    def disable_pause(self):
        self.game.paused = not self.game.paused
        self.game.level_loader.loaded_level.menu_showing = (
            not self.game.level_loader.loaded_level.menu_showing
        )
        self.game.level_loader.loaded_level.menu = (
            not self.game.level_loader.loaded_level.menu
        )
        self.game.level_loader.menu_present = not self.game.level_loader.menu_present

    def enable_pause(self):
        self.game.paused = not self.game.paused
        self.game.level_loader.loaded_level.menu_showing = True
        self.game.level_loader.menu_present = True
        self.game.level_loader.loaded_level.menu = True
        self.game.menu_render = self.game.level_loader.loaded_level.menu_render
        self.game.menu_update = self.game.level_loader.loaded_level.menu_update
