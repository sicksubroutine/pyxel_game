from __future__ import annotations
import esper as es

# components
from components.base import BaseComponent
from components.transform import Transform
from components.velocity import Velocity
from components.sprite import Sprite
from components.animation import Animation
from components.keyboard_controller import KeyboardController
from components.collider import Collider
from components.health import Health
from components.projectile_emitter import ProjectileEmitter
from components.projectile import Projectile
from components.audio import AudioComponent
from misc.logger import Logger


class Entity:
    def __init__(self, pool: EntityPool, *components: list) -> None:
        self.entity_id: int = es.create_entity(*components)
        self.pool: EntityPool = pool

    def __str__(self) -> str:
        return f"Entity {self.entity_id}"

    def __repr__(self) -> str:
        return f"<Entity {self.entity_id}>"

    def __int__(self) -> int:
        return self.entity_id

    def id(self) -> int:
        return self.entity_id

    def Tag(self, tag: str) -> None:
        self.pool.add_tag(self.entity_id, tag)

    def Group(self, group: str) -> None:
        self.pool.add_group(self.entity_id, group)

    def HasTag(self, tag: str) -> bool:
        return self.pool.has_tag(self.entity_id, tag) == self

    def BelongsToGroup(self, group: str) -> bool:
        return self.pool.belongs_to_group(self.entity_id, group)

    def has_component(self, component) -> bool:
        return self.pool.has_component(self, component)

    def remove_self(self) -> None:
        self.pool.remove_entity(self.entity_id)


class EntityPool:
    def __init__(self, game) -> None:
        self.game = game
        self.logger: Logger = game.logger
        self.logger.Log("Entity Pool initialized")
        self.entities: dict = {}
        self.tags: dict = {}
        self.groups: dict = {}
        self.possible_components: list = [
            Transform,
            Velocity,
            Sprite,
            Animation,
            KeyboardController,
            Collider,
            Health,
            ProjectileEmitter,
            Projectile,
            AudioComponent,
        ]

    def create_entity(self, *components: list) -> Entity:
        entity: Entity = Entity(self, *components)
        self.logger.Log(
            f"Creating entity {entity.entity_id} with components {components}"
        )
        self.logger.Log(self.game.level_loader.loaded_level.level_name)
        self.entities[entity.entity_id] = entity
        return entity

    def get_id(self, entity: Entity) -> int:
        return entity.entity_id

    def add_tag(self, entity_id: int, tag: str) -> None:
        self.tags[tag] = entity_id

    def remove_tag(self, tag: str) -> None:
        del self.tags[tag]

    def add_group(self, entity_id: int, group: str) -> None:
        if group not in self.groups:
            self.groups[group] = []
        self.groups[group].append(entity_id)

    def remove_group(self, entity_id: int, group: str) -> None:
        self.groups[group].remove(entity_id)
        if len(self.groups[group]) == 0:
            del self.groups[group]

    def get_group(self, group: str) -> list:
        if group not in self.groups:
            return []
        return self.groups[group]

    def has_tag(self, entity_id: int, tag: str) -> None | bool:
        if tag not in self.tags:
            return False
        elif self.tags[tag] == entity_id:
            return True
        else:
            return False

    def belongs_to_group(self, entity_id: int, group: str) -> None | bool:
        if group not in self.groups:
            return False
        elif entity_id in self.groups[group]:
            return True
        else:
            return False

    def has_component(self, entity: Entity, component: BaseComponent) -> bool:
        return es.has_component(entity.entity_id, component)

    def get_entity_from_id(self, entity_id: int) -> None | Entity:
        for entity in self.entities:
            if entity == entity_id:
                entity = self.entities[entity]
                return entity
        return None

    def remove_entity(self, entity_id: int, components: bool = True) -> None:
        if entity_id not in self.entities:
            return
        for group in self.groups.copy():
            if entity_id in self.groups[group]:
                self.groups[group].remove(entity_id)
                if len(self.groups[group]) == 0:
                    del self.groups[group]
        for tag in self.tags.copy():
            if self.tags[tag] == entity_id:
                del self.tags[tag]
        del self.entities[entity_id]
        if components:
            for component in self.possible_components:
                if es.has_component(entity_id, component):
                    es.remove_component(entity_id, component)
            es.delete_entity(entity_id, immediate=True)

    def clear_all_entities_in_group(self, group: str) -> None:
        if group not in self.groups:
            return
        entities = self.groups[group].copy()
        for entity_id in entities:
            self.remove_entity(entity_id, components=True)

    def clear_all_entities(self) -> None:
        for entity_id in self.entities.copy():
            self.remove_entity(entity_id, components=False)

    def entity_has_component(self, entity_id: int, component) -> bool:
        self.logger.Log(f"Checking if {entity_id} has {component}")
        return es.has_component(int(entity_id), component)

    def entity_get_component(self, entity_id: int, component) -> None | BaseComponent:
        return es.component_for_entity(int(entity_id), component)

    def get_list_of_entities(self) -> list:
        # collect a list of entity ids and any groups they may belong to
        entities = []
        for entity_id in self.entities:
            entity = self.entities[entity_id]
            groups = []
            for group in self.groups:
                if entity_id in self.groups[group]:
                    groups.append(group)
            entities.append({"entity": entity_id, "groups": groups})
        return entities
