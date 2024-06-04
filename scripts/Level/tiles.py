import os
import json
import pygame
import math
from scripts.Utils.settings import *
from scripts.Utils.utils import trim_surface
from scripts.GameObjects.platform import MovingPlatform
from scripts.GameObjects.collectable import Collectable
from scripts.GameObjects.trap import Trap
from scripts.GameObjects.goal import Goal
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
            objects = ["player", "collectable", "plat_horizontal", "plat_select", "plat_vertical", "enemy", "goal"]
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
            return surf
        
class Tilemap:
    def __init__(self, game, tilemap):
        self.tmap = os.path.join(assets_folder, "maps", tilemap + ".json")
        with open(self.tmap) as tm:
            self.json = json.load(tm)
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial',15)
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
        
    def load_layers(self):
        self.prepare_layers()
        self.load_game_object_layer()
        self.load_tile_layers()
        
    def prepare_layers(self):
        for layer in self.json["layers"]:
            self.layers.update({layer["name"]:{
                "group":pygame.sprite.Group(),
                "data": layer.get("data",[]),
                }})
            
    def load_game_object_layer(self):
        #print(self.tmap)
        game_objects_layer = self.layers["gameObjects"]
        paths = self.get_paths()
        if game_objects_layer:
            game_objects_layer["moving_platforms"] = pygame.sprite.Group()
            visited = set()  # Keep track of visited tiles
            
            for index, tile_id in enumerate(game_objects_layer["data"]):
                if tile_id != 0 and index not in visited:
                    object_type = self.get_tile_surface(tile_id)
                    if object_type == "plat_select":
                        platform_tiles = self.flood_fill(game_objects_layer["data"], index, visited)
                        if platform_tiles:
                            # delete selector tiles
                            for tile in platform_tiles:
                                game_objects_layer["data"][tile] = 0
                                
                            
                                tile_neighbors = self.get_neighbors(tile)
                                for path in paths:
                                    for tile_neighbor in tile_neighbors:
                                        if tile_neighbor in path:
                                            path, direction = self.convert_path(path)
                                            self.create_moving_platform(platform_tiles,path,direction)
                                            break
                    
                    elif object_type == "collectable":
                        self.create_collectable(index)
                        
                    # elif object_type == "trap":
                    #     self.create_trap(index)
                        
                    # elif object_type == "goal":
                    #     self.create_goal(index) 
                        
    def convert_path(self, path):
        tile_size = self.tile_height
        width = self.width
        converted_path = []
        direction = None
        
        for step in path:
            row = step // width
            col = step % width
            converted_path.append([col*tile_size,row*tile_size])
            
        if converted_path[0][0] == converted_path[1][0]:
            direction = "vertical"
            converted_path.sort(key=lambda x: x[1])
        elif converted_path[0][1] == converted_path[1][1]:
            direction = "horizontal"
            converted_path.sort(key=lambda x: x[0])
        return converted_path,direction
    
    def get_paths(self):
        game_objects_offset = 0
        for tileset in self.tilesets:
            if tileset[1].name == "game_objects":
                game_objects_offset = tileset[0]-1
        gameObjects = self.layers["gameObjects"]["data"]
        all_path_tiles = []
        paths = []
        visited = set()
        for index, gameObject in enumerate(gameObjects):
            if gameObject == 3+game_objects_offset:
                all_path_tiles.append({index:"plat_horizontal"})
            if gameObject == 5+game_objects_offset:
                all_path_tiles.append({index:"plat_vertical"})
        for path_tile in all_path_tiles:
            index = list(path_tile.keys())[0]
            if index not in visited:
                path = []
                stack = [index]
                while stack:
                    current_index = stack.pop()
                    if current_index not in visited:
                        visited.add(current_index)
                        path.append(current_index)
                        neighbors = self.get_neighbors(current_index)
                        for neighbor in neighbors:
                            if neighbor in [list(d.keys())[0] for d in all_path_tiles]:
                                stack.append(neighbor)
                paths.append(path)
                
        return paths
        
    def load_tile_layers(self):
        # Handle other layers
        for layer in self.layers:
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
    
    def flood_fill(self, data, start_index, visited):
        platform_tiles = []
        stack = [start_index]
        while stack:
            index = stack.pop()
            if index not in visited:
                visited.add(index)
                object_type = self.get_tile_surface(data[index])
                if object_type == "plat_select":
                    platform_tiles.append(index)
                    stack.extend(self.get_neighbors(index))

        return platform_tiles
    
    def is_valid_index(self, index):
            row = index // self.width
            col = index % self.width
            return 0 <= row < self.height and 0 <= col < self.width
        
    def get_neighbors(self, index, horizontal=True, vertical=True):
            neighbors = []
            if vertical:
                if self.is_valid_index(index - self.width):
                    neighbors.append(index - self.width)  # Up
                if self.is_valid_index(index + self.width):
                    neighbors.append(index + self.width)  # Down
            if horizontal:
                if self.is_valid_index(index - 1) and (index % self.width) > 0:
                    neighbors.append(index - 1)  # Left
                if self.is_valid_index(index + 1) and (index % self.width) < self.width - 1:
                    neighbors.append(index + 1)  # Right
            return neighbors
        
    def create_moving_platform(self, platform_tiles, path, direction):
        moving_platform = MovingPlatform(self.game, self, platform_tiles, self.tile_width, self.tile_height, PLATFORM_SPEED, path, direction)
        self.layers["gameObjects"]["moving_platforms"].add(moving_platform)
        
    def index_to_coordinates(self,index):
        row = index // self.width
        col = index % self.width
        x = col*self.tile_width
        y = row*self.tile_height
        return x,y

    def create_collectable(self, index):
        x,y = self.index_to_coordinates(index)
        collectable = Collectable(self.game, x, y,)
        self.layers["gameObjects"]["group"].add(collectable)
        
    # def create_trap(self, index):
    #     x,y = self.index_to_coordinates(index)
    #     surf = self.get_tile_surface(self.layers["solid"]["data"]["index"])
    #     rect = pygame.rect.Rect(x,
    #                             y,
    #                             self.tile_width,
    #                             self.tile_height,
    #                         )
    #     trap = Trap(self.game, x, y, surf, rect)
    #     self.layers["gameObjects"]["group"].add(trap)
        
    # def create_goal(self, index):
    #     x, y = self.index_to_coordinates(index)
    #     surf = self.get_tile_surface(self.layers["solid"]["data"]["index"])
    #     rect = pygame.rect.Rect(x,
    #                             y,
    #                             self.tile_width,
    #                             self.tile_height,
    #                         )
    #     goal = Goal(self.game, x, y, surf, rect)
    #     self.layers["gameObjects"]["group"].add(goal) 
        
    def get_tile_surface(self, tile_id):
        for firstgid, tileset in self.tilesets:
            if tile_id >= firstgid and tile_id <=firstgid+tileset.tile_count:
                tile_index = tile_id - firstgid
                return tileset.get_tile_surface(tile_index)
        return None

    def get_layers(self):
        return self.layers


