import os
import json
import pygame
import math
from scripts.Utils.settings import *
from scripts.Utils.utils import trim_surface
from scripts.GameObjects.platform import MovingPlatform
scripts_folders = os.path.dirname(__file__)
game_folder = os.getcwd()
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
        if self.name == "game_objects":
            objects = ["player","collectable","plat_horizontal","plat_select","plat_vertical","enemy","goal"]
            return objects[tile_id]
        else:   
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
        self.tmap = os.path.join(assets_folder, "maps", tilemap + ".json")
        with open(self.tmap) as tm:
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

        #self.load_layers()
        
    def load_layers(self):
        self.prepare_layers()
        self.load_game_object_layer()
        self.load_tile_layers()
        
    def prepare_layers(self):
        for layer in self.json["layers"]:
            #print(layer["name"])
            self.layers.update({layer["name"]:{
                "group":pygame.sprite.Group(),
                "data": layer.get("data",[]),
                }})
            #if layer["name"] == "solid":
            #    print(self.layers[layer["name"]]["data"])
            
    def load_game_object_layer(self):
        print(self.tmap)
        game_objects_layer = self.layers["gameObjects"]

        if game_objects_layer:
            game_objects_layer["moving_platforms"] = pygame.sprite.Group()
            
            visited = set()  # Keep track of visited tiles
            for index, tile_id in enumerate(game_objects_layer["data"]):
                if tile_id != 0 and index not in visited:
                    object_type = self.get_tile_surface(tile_id)
                    if object_type == "plat_select":
                        platform_tiles = self.flood_fill(game_objects_layer["data"], index, visited)
                        print(platform_tiles)
                        if platform_tiles:
                            paths, direction = self.generate_paths(platform_tiles)
                            self.create_moving_platform(platform_tiles,paths,direction)
                            
                            #delete selector tiles
                            for tile in platform_tiles:
                                #print(tile)
                                game_objects_layer["data"][tile] = 0
                        
    def load_tile_layers(self):
        # Handle other layers
        for layer in self.layers:
            
            #layer_name = layer["name"]
            if layer != "gameObjects":
                for index, tile_id in enumerate(self.layers[layer]["data"]):
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
                            self.layers[layer]["group"].add(tile_sprite)
                            
    def generate_paths(self, platform_tiles):
        paths = []
        direction = None

        def dfs(index, path):
            nonlocal direction
            row = index // self.width
            col = index % self.width
            path.append((col, row))

            neighbors = [
                (col, row - 1),  # Up
                (col, row + 1),  # Down
                (col - 1, row),  # Left
                (col + 1, row),  # Right
            ]

            for neighbor_col, neighbor_row in neighbors:
                neighbor_index = neighbor_row * self.width + neighbor_col
                if (
                    0 <= neighbor_col < self.width
                    and 0 <= neighbor_row < self.height
                    and neighbor_index in platform_tiles
                    and (neighbor_col, neighbor_row) not in path
                ):
                    if direction is None:
                        if neighbor_col != col:
                            direction = "horizontal"
                        elif neighbor_row != row:
                            direction = "vertical"
                    dfs(neighbor_index, path)

        for tile_index in platform_tiles:
            path = []
            dfs(tile_index, path)
            if path:
                paths.append(path)

        return paths, direction

    def flood_fill(self, data, start_index, visited):
        width = self.width
        height = self.height
        platform_tiles = []

        def is_valid_index(index):
            row = index // width
            col = index % width
            return 0 <= row < height and 0 <= col < width

        def get_neighbors(index):
            neighbors = []
            if is_valid_index(index - width):
                neighbors.append(index - width)  # Up
            if is_valid_index(index + width):
                neighbors.append(index + width)  # Down
            if is_valid_index(index - 1) and (index % width) > 0:
                neighbors.append(index - 1)  # Left
            if is_valid_index(index + 1) and (index % width) < width - 1:
                neighbors.append(index + 1)  # Right
            return neighbors

        stack = [start_index]
        while stack:
            index = stack.pop()
            if index not in visited:
                visited.add(index)
                object_type = self.get_tile_surface(data[index])
                if object_type == "plat_select":
                    platform_tiles.append(index)
                    stack.extend(get_neighbors(index))

        return platform_tiles
    
    def create_moving_platform(self, platform_tiles, paths, direction):
        moving_platform = MovingPlatform(self.game, self, platform_tiles, self.tile_width, self.tile_height, PLATFORM_SPEED, paths, direction)
        #print(moving_platform)
        self.layers["gameObjects"]["moving_platforms"].add(moving_platform)
        #print(self.layers["gameObjects"]["moving_platforms"])
            
    def get_tile_surface(self, tile_id):
        for firstgid, tileset in self.tilesets:
            if tile_id >= firstgid and tile_id <=firstgid+tileset.tile_count:
                tile_index = tile_id - firstgid
                return tileset.get_tile_surface(tile_index)
        return None

    def get_layers(self):
        return self.layers


