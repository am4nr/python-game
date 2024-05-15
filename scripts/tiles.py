import os
import json
import pygame
import math

scripts_folders = os.path.dirname(__file__)
game_folder = os.path.join(scripts_folders, os.pardir)
assets_folder = os.path.join(game_folder, "assets")


class Tileset:
    def __new__(cls, game, tileset, **kwargs):
        self = object.__new__(Tileset)
        tset = os.path.join(assets_folder, "tilesets", tileset + ".json")

        with open(tset) as ts:
            self.json = json.load(ts)

        self.game = game
        self.name = self.json["name"]
        self.image = game.assets.get("Image", self.json["image"])
        self.type = self.json["type"]
        self.image_height = self.json["imageheight"]
        self.image_width = self.json["imagewidth"]
        self.tile_height = self.json["tileheight"]
        self.tile_width = self.json["tilewidth"]
        self.columns = self.json["columns"]
        self.tile_count = self.json["tilecount"]
        self.margin = self.json["margin"]
        self.spacing = self.json["spacing"]
        self.animation_frames = self.json["tiles"] if "tiles" in self.json else []
        self.tiles = {}
        self.tiled_version = self.json["tiledversion"]
        self.version = self.json["version"]
        self.load_tiles()
        return self

    def __init__(self):
        pass

    def load_tiles(self):
        for tile in range(0, self.tile_count):
            row = math.floor(tile / self.columns)
            col = math.floor(tile - row * self.columns)
            surf = pygame.Surface((self.tile_width, self.tile_height)).convert_alpha()
            
            self.tiles[tile] = surf.blit(
                self.image,
                (0, 0),
                (
                    (col * self.tile_width),
                    (row * self.tile_height),
                    self.tile_width,
                    self.tile_height,
                ),
            )

    def __repr__(self):
        return f"{{name: {self.name}}}, {{image: {self.image}}}, {{type: {self.type}}}, {{image_height: {self.image_height}}}, {{image_width: {self.image_width}}}, {{columns: {self.columns}}}, {{tile_height: {self.tile_height}}}, {{tile_width: {self.tile_width}}}, {{tile_count: {self.tile_count}}}, {{margin: {self.margin}}}, {{spacing: {self.spacing}}}, {{tiles: {self.tiles}}}, {{tiled_version: {self.tiled_version}}}, {{version: {self.version}}}"

    def get_tiles(self):
        return self.tiles
class Tilemap:
    def __new__(cls, game, tilemap, **kwargs):
        self = object.__new__(Tilemap)
        tmap = os.path.join(assets_folder, "maps", tilemap + ".json")

        with open(tmap) as tm:
            self.json = json.load(tm)

        self.game = game
        self.compression_level = self.json["compressionlevel"]
        self.height = self.json["height"]
        self.width = self.json["width"]
        self.infinite = self.json["infinite"]
        self.layers = self.json["layers"]
        self.next_layer_id = self.json["nextlayerid"]
        self.next_object_id = self.json["nextobjectid"]
        self.orientation = self.json["orientation"]
        self.render_order = self.json["renderorder"]
        self.tile_height = self.json["tileheight"]
        self.tile_width = self.json["tilewidth"]
        self.tilesets = []

        for tileset in self.json["tilesets"]:
            source = tileset["source"]
            firstgid = tileset["firstgid"]
            name = os.path.splitext(source)[0]
            data = {"name": name, "offset": firstgid - 1}
            self.tilesets.append(data)

        self.type = self.json["type"]
        self.tiled_version = self.json["tiledversion"]
        self.version = self.json["version"]
        return self

    def __init__(self):
        self.loadTilesets(self.game)

    def __repr__(self):
        return f"{{compression_level: {self.compression_level}}}, {{height: {self.height}}}, {{infinite: {self.infinite}}}, {{layers: {{...}}}}, {{next_layer_id: {self.next_layer_id}}}, {{next_object_id: {self.next_object_id}}}, {{orientation: {self.orientation}}}, {{render_order: {self.render_order}}}, {{tile_height: {self.tile_height}}}, {{tile_width: {self.tile_width}}}, {{tilesets: {self.tilesets}}}, {{type: {self.type}}}, {{tiled_version: {self.tiled_version}}}, {{version: {self.version}}}"

    def loadTilesets(self, game):
        if "tileset" not in game.assets.collections:
            game.assets.collections["tileset"] = {}

        for tileset in self.tilesets:
            if tileset["name"] not in game.assets.collections["tileset"]:
                game.assets.collections["tileset"][tileset["name"]] = game.assets.get("Tileset", tileset["name"])


class Level:
    def __new__(cls, game, tilemap, **kwargs):
        self = object.__new__(Level)
        self.game = game
        self.layers = tilemap.layers
        self.tilesets = tilemap.tilesets
        self.tiles = []
        self.loadTiles()
        
    def loadTiles(self):
        counter = 0
        # hier ist es noch ein Tilemap.Tilesets dict
        for ts in self.tilesets:
            #hier wird es eine Tileset Instanz
            tileset = self.game.assets.get("Tileset", ts["name"])
            # print(tileset.get_tiles())
            """ for tile in tileset.get_tiles:
                self.tiles[counter] = self.tile
                counter += 1
        print(self.tiles)