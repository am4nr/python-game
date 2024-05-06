import os
import json

scripts_folders = os.path.dirname(__file__)
game_folder = os.path.join(scripts_folders, os.pardir)
assets_folder = os.path.join(game_folder, "assets")


class Tileset:
    def __new__(cls, tileset):
        self = object.__new__(Tileset)
        tset = os.path.join(assets_folder, "tilesets", tileset + ".json")

        with open(tset) as ts:
            self.json = json.load(ts)

        self.name = self.json["name"]
        self.image = self.json["image"]
        self.type = self.json["type"]
        self.image_height = self.json["imageheight"]
        self.image_width = self.json["imagewidth"]
        self.columns = self.json["columns"]
        self.tile_height = self.json["tileheight"]
        self.tile_width = self.json["tilewidth"]
        self.tile_count = self.json["tilecount"]
        self.margin = self.json["margin"]
        self.spacing = self.json["spacing"]
        self.tiles = self.json["tiles"] if "tiles" in self.json else []
        self.tiled_version = self.json["tiledversion"]
        self.version = self.json["version"]
        return self

    def __init__(self, tileset):
        pass

    def __repr__(self):
        return f"{{name: {self.name}}}, {{image: {self.image}}}, {{type: {self.type}}}, {{image_height: {self.image_height}}}, {{image_width: {self.image_width}}}, {{columns: {self.columns}}}, {{tile_height: {self.tile_height}}}, {{tile_width: {self.tile_width}}}, {{tile_count: {self.tile_count}}}, {{margin: {self.margin}}}, {{spacing: {self.spacing}}}, {{tiles: {self.tiles}}}, {{tiled_version: {self.tiled_version}}}, {{version: {self.version}}}"


class Tilemap:
    def __init__(self, tilemap, game):
        tmap = os.path.join(assets_folder, "maps", tilemap + ".json")

        with open(tmap) as tm:
            self.json = json.load(tm)

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
            data = {"name": name, "firstgid": firstgid}
            self.tilesets.append(data)

        self.type = self.json["type"]
        self.tiled_version = self.json["tiledversion"]
        self.version = self.json["version"]
        game.flyweight("map", self)

    def __repr__(self):
        return f"{{compression_level: {self.compression_level}}}, {{height: {self.height}}}, {{infinite: {self.infinite}}}, {{layers: {self.layers}}}, {{next_layer_id: {self.next_layer_id}}}, {{next_object_id: {self.next_object_id}}}, {{orientation: {self.orientation}}}, {{render_order: {self.render_order}}}, {{tile_height: {self.tile_height}}}, {{tile_width: {self.tile_width}}}, {{tilesets: {self.tilesets}}}, {{type: {self.type}}}, {{tiled_version: {self.tiled_version}}}, {{version: {self.version}}}"
