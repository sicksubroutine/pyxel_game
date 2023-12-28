import esper as es
import traceback

from misc.entity import EntityPool
from misc.logger import Logger
from misc.asset_store import AssetStore

from components.health import Health
from components.sprite import Sprite
from components.projectile import Projectile
from components.transform import Transform
from components.audio import AudioComponent, AudioChannel


class DamageSystem:
    def __init__(self, game):
        self.game = game
        self.pool: EntityPool = game.pool
        self.logger: Logger = game.logger
        self.asset_store: AssetStore = game.asset_store

    def on_collision(self, entity1: dict, entity2: dict) -> None:
        entities = {"bullet": None, "enemy": None, "player": None}

        for entity in [entity1, entity2]:
            if entity["group"] == "bullet":
                entities["bullet"] = entity["entity"]
            elif entity["group"] == "enemies":
                entities["enemy"] = entity["entity"]
            elif entity["group"] == "player":
                entities["player"] = entity["entity"]

        if entities["bullet"] and entities["bullet"] not in self.pool.entities:
            return

        if entities["enemy"] and entities["enemy"] not in self.pool.entities:
            return

        if entities["player"] and entities["player"] not in self.pool.entities:
            return
        if entities["player"]:
            sprite = es.component_for_entity(entities["player"], Sprite)
        # direct hit between player and enemy
        if entities["player"] and entities["enemy"]:
            if sprite.hit_flash > 0:
                # player is invulnerable for a short time after being hit
                return
            sprite.hit_flash = 120
            self.damage_to_enemy(entities["enemy"], 25)
            self.damage_to_player(entities["player"], 25)

        # projectile hit player
        if entities["player"] and entities["bullet"]:
            projectile = es.component_for_entity(entities["projectile"], Projectile)
            if projectile.is_friendly:
                return
            if sprite.hit_flash > 0:
                # player is invulnerable for a short time after being hit
                return
            sprite.hit_flash = 120
            damage = projectile.hit_damage
            self.damage_to_player(entities["player"], damage)
            self.pool.remove_entity((entities["bullet"]))

        # projectile hit enemy
        if entities["enemy"] and entities["bullet"]:
            projectile = es.component_for_entity(entities["bullet"], Projectile)
            if not projectile.is_friendly:
                return
            damage = projectile.hit_damage
            self.damage_to_enemy(entities["enemy"], damage)
            self.pool.remove_entity((entities["bullet"]))

    def damage_to_enemy(self, enemy, damage=0.1) -> None:
        try:
            if enemy not in self.pool.entities:
                return
            position = es.component_for_entity(enemy, Transform).position
            enemy_health = es.component_for_entity(enemy, Health)
            enemy_sprite = es.component_for_entity(enemy, Sprite)
            size = enemy_sprite.width
            es.dispatch_event(
                "sparks", position.x + enemy_sprite.width / 2, position.y, size
            )
            enemy_sprite.hit_flash = 5
            if enemy_health.is_god_mode:
                return
            enemy_health.current_health -= damage
            if enemy_health.current_health < 1:
                center_pos_x = position.x + enemy_sprite.width / 2
                center_pos_y = position.y + enemy_sprite.height / 2
                size = 25 if size == 8 else 100
                es.dispatch_event("explosion", center_pos_x, center_pos_y, size)
                self.pool.remove_entity(enemy)
        except Exception as e:
            self.logger.Log(traceback.format_exc())

    def damage_to_player(self, player, damage=0.1) -> None:
        try:
            if player not in self.pool.entities:
                return
            player_health = es.component_for_entity(player, Health)
            audio = AudioComponent(
                channel=int(AudioChannel.EFFECT_CHANNEL.value) + 1,
                audio_id=self.asset_store.get_sound("hit"),
                loop=False,
            )
            es.add_component(player, audio)
            if player_health.is_god_mode:
                return
            player_health.current_health -= damage
            if player_health.current_health <= 0:
                es.dispatch_event("player_death")
        except Exception as e:
            self.logger.Log(traceback.format_exc())
