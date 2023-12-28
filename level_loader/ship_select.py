from level_loader.base import BaseMenu
from systems.player_system import PlayerSystem
from misc.logger import Logger
from misc.asset_store import AssetStore
from components.color import colors
from components.sprite import Sprite, SpriteLayer
import pyxel as px


class ShipSelect(BaseMenu):
    def __init__(self, game):
        super().__init__(game)
        self.level_loader = game.level_loader
        self.asset_store: AssetStore = game.asset_store
        self.player_system: PlayerSystem = game.player_system
        self.level_name = "Ship Selection"
        self.assets = [
            {
                "asset_type": "resource",
                "asset_id": "assets",
                "path": "./assets/assets.pyxres",
            },
            {
                "asset_type": "sound",
                "asset_id": "shoot",
                "number": 0,
            },
            {
                "asset_type": "sound",
                "asset_id": "hit",
                "number": 1,
            },
            {
                "asset_type": "sound",
                "asset_id": "explode",
                "number": 2,
            },
            {
                "asset_type": "sound",
                "asset_id": "selection",
                "number": 3,
            },
        ]
        self.player_sprite: Sprite = Sprite()
        self.potential_ships = {
            0: {"u": 8, "v": 0},
            1: {"u": 8, "v": 8},
            2: {"u": 8, "v": 16},
            3: {"u": 8, "v": 24},
            4: {"u": 8, "v": 32},
        }
        self.selected_ship = 0
        self.ship_selected = False
        self.show_ship_selection = 500

    def menu_update(self):
        if self.ship_selected:
            self.show_ship_selection -= 5
            if self.show_ship_selection <= 0:
                self.player_sprite = Sprite(
                    width=8,
                    height=8,
                    img=0,
                    default_u=8,
                    u=self.potential_ships[self.selected_ship]["u"],
                    v=self.potential_ships[self.selected_ship]["v"],
                    layer=SpriteLayer.PLAYER_LAYER,
                    is_fixed=False,
                )
                self.player_system.player_sprite = self.player_sprite
                self.level_loader.next_level()
            return
        if px.btnp(px.KEY_DOWN):
            if self.selected_ship < 4:
                self.selected_ship += 1
            else:
                self.selected_ship = 0
        elif px.btnp(px.KEY_UP):
            if self.selected_ship > 0:
                self.selected_ship -= 1
            else:
                self.selected_ship = 4
        if px.btnp(px.KEY_RETURN):
            px.play(ch=0, snd=self.asset_store.get_sound("selection"), loop=False)
            self.ship_selected = True

    def menu_render(self):
        px.rect(26, 8, 12, 52, colors["BLACK"])
        px.rectb(26, 8, 12, 52, colors["WHITE"])
        if self.show_ship_selection % 2 == 0 and self.show_ship_selection > 0:
            px.rectb(26, 9 + self.selected_ship * 10, 12, 10, colors["RED"])
        for index, ship in enumerate(self.potential_ships):
            px.blt(
                28,
                10 + index * 10,
                0,
                self.potential_ships[ship]["u"],
                self.potential_ships[ship]["v"],
                8,
                8,
                colors["BLACK"],
            )
