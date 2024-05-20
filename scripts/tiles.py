import os
import json
import pygame
import math

scripts_folders = os.path.dirname(__file__)
game_folder = os.path.join(scripts_folders, os.pardir)
assets_folder = os.path.join(game_folder, "assets")


# akzeptiert ein tileset, welches aus Tiled als JSON exportiert wurde
class Tileset:
    def __init__(self, game, tileset):
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
        self.tiles = []
        self.tiled_version = self.json["tiledversion"]
        self.version = self.json["version"]
        self.load_tiles()

    # Tileset wird in Tiles (Sprites) gesplittet
    def load_tiles(self):
        for tile in range(self.tile_count):
            row = math.floor(tile / self.columns)
            col = math.floor(tile - row * self.columns)
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
            #self.game.assets.get("Sprite",surf)
            self.tiles.append(self.game.assets.get("Sprite",surf))

    def get_tiles(self):
        return self.tiles

# Tile Klasse wird nicht mehr benutzt
""" class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def set_position(self, x, y):
        self.rect.topleft = (x, y) """


class Tilemap:
    def __init__(self, game, tilemap):
        tmap = os.path.join(assets_folder, "maps", tilemap + ".json")

        with open(tmap) as tm:
            self.json = json.load(tm)

        self.game = game
        self.compression_level = self.json["compressionlevel"]
        self.height = self.json["height"]
        self.width = self.json["width"]
        self.infinite = self.json["infinite"]
        self.layers_data = self.json["layers"]
        self.next_layer_id = self.json["nextlayerid"]
        self.next_object_id = self.json["nextobjectid"]
        self.orientation = self.json["orientation"]
        self.render_order = self.json["renderorder"]
        self.tile_height = self.json["tileheight"]
        self.tile_width = self.json["tilewidth"]
        self.tilesets = []
        self.tiles = {}
        self.layers = {}

        for tileset in self.json["tilesets"]:
            source = tileset["source"]
            firstgid = tileset["firstgid"]
            name = os.path.splitext(os.path.basename(source))[0]
            data = {"name": name, "firstgid": firstgid}
            self.tilesets.append(data)

        self.type = self.json["type"]
        self.tiled_version = self.json["tiledversion"]
        self.version = self.json["version"]
        self.load_tilesets()
        self.load_layers()

    def load_tilesets(self):
        for tileset in self.tilesets:
            tileset_obj = self.game.assets.get("Tileset", tileset["name"])
            print(self.tilesets)
            for index, tile in enumerate(tileset_obj.get_tiles()):
                firstgid = tileset['firstgid']
                print(f"{tileset['name']}")
                print(f"firstgid: {tileset['firstgid']}")
                print(f"index: {index}")
                print(tile)
                self.tiles[firstgid+index] = tile
            #self.tilesset[tileset["name"]] = {"firstgid":tileset["firstgid"], "tileset": tileset_obj}
            #self.tiles.append((tileset["firstgid"], tileset_obj))
        print(self.tiles)
        
    def load_layers(self):
        width = self.width
        layers = self.layers_data
        
        #print(layers)
        for layer in layers:
            #print(layer)
            layername = layer["name"]
            #print(layername)
            self.layers[layername] = {"group": pygame.sprite.Group(), "data": layer.get("data", [])}
            for index, tile_id in enumerate(layer["data"]):
                if tile_id != 0:
                    tile = self.get_tile(tile_id)
                    col = index % width
                    row = index // width
                    tile.rect = [col * self.tile_width, row * self.tile_height]
                    self.layers[layername]["group"].add(tile)
            
        print(self.layers)
        
    def get_tile(self, tile_id):
        return self.tiles[tile_id]
    
    def get_layers(self):
        return self.layers

class Level:
    def __init__(self, game, tilemap):
        self.game = game
        self.tilemap = Tilemap(game, tilemap)
        self.layers = {}
        #self.load_layers()

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
