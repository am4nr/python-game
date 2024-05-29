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

        # Load the "solid" layer first
        for layer in layers:
            if layer["name"] == "solid":
                self.layers["solid"] = {
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
                            self.layers["solid"]["group"].add(tile_sprite)
                break

        # Handle the "gameObjects" layer
        gameobjects_layer = None
        for layer in layers:
            if layer["name"] == "gameObjects":
                gameobjects_layer = layer
                break

        if gameobjects_layer:
            self.layers["gameObjects"] = {
                "group": pygame.sprite.Group(),
                "data": gameobjects_layer.get("data", []),
                "moving_platforms": [],
            }
            for index, tile_id in enumerate(gameobjects_layer["data"]):
                if tile_id == 64:  # Platform tile ID
                    # Get the tile surface from the solid layer
                    solid_tile_id = self.layers["solid"]["data"][index]
                    solid_tile_surf = self.get_tile_surface(solid_tile_id)

                    # Create a new sprite for the platform
                    col = index % self.width
                    row = index // self.width
                    platform_sprite = self.game.assets.get("Sprite", solid_tile_surf)
                    platform_sprite.rect = pygame.rect.Rect(
                        col * self.tile_width,
                        row * self.tile_height,
                        self.tile_width,
                        self.tile_height,
                    )

                    # Add the platform sprite to the game objects layer
                    self.layers["gameObjects"]["group"].add(platform_sprite)

                    # Find the path for the platform
                    path = []
                    self.find_platform_path(gameobjects_layer["data"], index, path)
                    if path:
                        moving_platform = MovingPlatform(platform_sprite, path, PLATFORM_SPEED)
                        self.layers["gameObjects"]["moving_platforms"].append(moving_platform)

        # Handle other layers
        for layer in layers:
            layername = layer["name"]
            if layername != "gameObjects" and layername != "solid":
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
                            
    def find_platform_path(self, data, start_index, path):
        width = self.width
        height = self.height
        path_tiles = [65, 64]  # Vertical and horizontal path tiles

        def is_valid_index(index):
            row = index // width
            col = index % width
            return 0 <= row < height and 0 <= col < width

        def get_neighbors(index):
            row = index // width
            col = index % width
            neighbors = []
            if is_valid_index(index - width):
                neighbors.append(index - width)  # Up
            if is_valid_index(index + width):
                neighbors.append(index + width)  # Down
            if is_valid_index(index - 1):
                neighbors.append(index - 1)  # Left
            if is_valid_index(index + 1):
                neighbors.append(index + 1)  # Right
            return neighbors

        def find_path(start):
            stack = [(start, [])]
            visited = set()

            while stack:
                current, current_path = stack.pop()
                if current not in visited:
                    visited.add(current)
                    tile_id = data[current]
                    if tile_id in path_tiles:
                        current_path.append(pygame.rect.Rect(
                            (current % width) * self.tile_width,
                            (current // width) * self.tile_height,
                            self.tile_width,
                            self.tile_height,
                        ))
                        for neighbor in get_neighbors(current):
                            if data[neighbor] in path_tiles:
                                stack.append((neighbor, current_path[:]))
                    else:
                        path.extend(current_path)

        find_path(start_index)
                            
    def get_tile_surface(self, tile_id):
        for firstgid, tileset in self.tilesets:
            if tile_id >= firstgid and tile_id <=firstgid+tileset.tile_count:
                tile_index = tile_id - firstgid
                return tileset.get_tile_surface(tile_index)
        return None

    def get_layers(self):
        return self.layers


