import os
import json
import pygame
import math
from scripts.utils import trim_surface
scripts_folders = os.path.dirname(__file__)
game_folder = os.path.join(scripts_folders, os.pardir)
assets_folder = os.path.join(game_folder, "assets")

class Tileset:
    def __init__(self, game, tileset):
        tset = os.path.join(assets_folder, "tilesets", tileset + ".json")

        with open(tset) as ts:
            self.json = json.load(ts)

        self.game = game
        self.name = self.json["name"]
        self.image = game.assets.get("Image", self.json["image"])
        self.tile_height = self.json["tileheight"]
        self.tile_width = self.json["tilewidth"]
        self.columns = self.json["columns"]
        self.tile_count = self.json["tilecount"]

    def get_tile_surface(self, tile_id):
        if tile_id < 0 or tile_id >= self.tile_count:
            return None

        row = math.floor(tile_id / self.columns)
        col = math.floor(tile_id - row * self.columns)
        surf = pygame.Surface(
            (self.tile_width, self.tile_height), pygame.SRCALPHA
        ).convert_alpha()
        surf.blit(
            self.image,
            (0, 0),
            (
                (col * self.tile_width),
                (row * self.tile_height),
                self.tile_width,
                self.tile_height,
            ),
        )
        return trim_surface(surf)

class Tilemap:
    def __init__(self, game, tilemap):
        tmap = os.path.join(assets_folder, "maps", tilemap + ".json")

        with open(tmap) as tm:
            self.json = json.load(tm)

        self.game = game
        self.width = self.json["width"]
        self.height = self.json["height"]
        self.tile_width = self.json["tilewidth"]
        self.tile_height = self.json["tileheight"]
        self.tilesets = []
        self.layers = {}

        for tileset in self.json["tilesets"]:
            source = tileset["source"]
            firstgid = tileset["firstgid"]
            name = os.path.splitext(os.path.basename(source))[0]
            tileset_obj = self.game.assets.get("Tileset", name)
            self.tilesets.append((firstgid, tileset_obj))

        self.load_layers()

    def load_layers(self):
        layers = self.json["layers"]

        for layer in layers:
            layername = layer["name"]
            self.layers[layername] = {
                "group": pygame.sprite.Group(),
                "data": layer.get("data", []),
            }
            for index, tile_id in enumerate(layer["data"]):
                if tile_id != 0:
                    tile_surf = self.get_tile_surface(tile_id)
                    if tile_surf is not None:
                        col = index % self.width
                        row = index // self.width
                        tile_sprite = self.game.assets.get("Sprite", tile_surf)
                        tile_sprite.rect = pygame.rect.Rect(
                            col * self.tile_width,
                            row * self.tile_height,
                            self.tile_width,
                            self.tile_height,
                        )
                        self.layers[layername]["group"].add(tile_sprite)

    def get_tile_surface(self, tile_id):
        for firstgid, tileset in self.tilesets:
            if tile_id >= firstgid:
                tile_index = tile_id - firstgid
                return tileset.get_tile_surface(tile_index)
        return None

    def get_layers(self):
        return self.layers


class Level:
    def __init__(self, game, tilemap):
        self.game = game
        self.tilemap = Tilemap(game, tilemap)
        self.layers = {}


"""     def load_layers(self):
        width = self.tilemap.width

        for layer in self.tilemap.layers:
            layername = layer["name"]
            self.layers[layername] = {
                "group": pygame.sprite.Group(),
                "data": layer.get("data", []),
            }

            for index, tile_id in enumerate(layer["data"]):
                if tile_id != 0:
                    tile = self.tilemap.get_tile(tile_id)
                    if tile:
                        col = index % width
                        row = index // width
                        tile.rect = [col * self.tilemap.tile_width,
                            row * self.tilemap.tile_height]
                        self.layers[layername]["group"].add(tile)

    def get_layers(self):
        return self.layers """
