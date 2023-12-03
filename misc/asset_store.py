# Where assets are stored
import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D
import glm
from misc.entity import EntityPool
from components.sprite import Sprite, SpriteLayer
from components.transform import Transform
from misc.logger import Logger


class TileMap:
    def __init__(
        self, pool: EntityPool, tile_size: int, tile_scale: float, asset_id: str
    ) -> None:
        self.pool: EntityPool = pool
        self.tile_size = tile_size
        self.tile_scale = tile_scale
        self.map_width = 0  # in pixels
        self.map_height = 0  # in pixels
        self.tile_width = 0  # in tiles
        self.tile_height = 0  # in tiles
        self.asset_id = asset_id

    def load_map(self, file_path) -> None:
        with open(file_path, "r") as f:
            map_data = [[int(tile) for tile in line.split(",")] for line in f]
        scale = self.tile_size * self.tile_scale
        self.map_width = len(map_data[0]) * scale
        self.map_height = len(map_data) * scale

        self.tile_width = len(map_data[0])
        self.tile_height = len(map_data)

        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                tile_id = int(map_data[y][x])
                tile_row = tile_id // 10
                tile_col = tile_id % 10
                src_rect = pg.Rect(
                    tile_col * self.tile_size,
                    tile_row * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )

                entity = self.pool.create_entity(
                    Transform(
                        glm.vec2(x * scale, y * scale),
                        glm.vec2(self.tile_scale, self.tile_scale),
                        0.0,
                    ),
                    Sprite(
                        self.asset_id,
                        self.tile_size,
                        self.tile_size,
                        SpriteLayer.BACKGROUND_LAYER,
                        False,
                        src_rect,
                    ),
                )
                entity.Group("tilemap")

    def unload_map(self) -> None:
        for entity in self.pool.groups["tilemap"]:
            self.pool.remove_entity(entity)


class AssetStore:
    def __init__(self, logger: Logger) -> None:
        self.assets = {}
        self.fonts = {}
        self.sounds = {}
        self.logger = logger
        self.logger.Log("Asset Store created")

    def clear_assets(self) -> None:
        for asset in self.assets:
            asset = None
        self.assets.clear()
        for font in self.fonts:
            font = None
        self.fonts.clear()
        for sound in self.sounds:
            sound = None
        self.sounds.clear()

    def add_texture(self, name, file_path) -> None:
        texture: pg.Surface = pg.image.load(file_path).convert_alpha()
        self.assets[name] = texture

    def get_texture(self, name) -> pg.Surface:
        return self.assets[name]

    def add_font(self, name, file_path, size) -> None:
        self.fonts[name]: pg.font.Font = pg.font.Font(file_path, size)

    def get_font(self, name) -> pg.font.Font:
        return self.fonts[name]

    def add_sound(self, name, file_path) -> None:
        self.sounds[name] = pg.mixer.Sound(file_path)

    def get_sound(self, name) -> pg.mixer.Sound:
        return self.sounds[name]
