import pygame
import os
import sys
from scripts.tiles import Tilemap, Tileset

# Dateisystem
scripts_folders = os.path.dirname(__file__)
game_folder = os.path.join(scripts_folders, os.pardir)
assets_folder = os.path.join(game_folder, "assets")


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


# to do: def get_tiles_dict()


# Flyweight als singleton, damit nicht mehr als ein Flyweight erstellt werden kann -> jede instanz von Flyweight ist die selbe
class Flyweight:
    __instance = None
    collections = {
        "sprite": {},
        "animation": {},
        "audio": {},
        "tileset": {},
        "tilemap": {},
    }

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __repr__(self):
        return f"assets:\n {{sprite: {self.collections['sprite']}}},\n {{animation: {self.collections['animation']}}},\n {{audio: {self.collections['audio']}}},\n {{tileset: {self.collections['tileset']}}},\n {{tilemap: {self.collections['tilemap']}}}"


class Asset:
    def __new__(cls, asset_type, asset, **kwargs):
        self = Flyweight.collections.get(asset_type.lower()).get(asset)
        if self is None:
            self = Flyweight.collections[asset_type.lower()][asset] = str_to_class(
                asset_type
            ).__new__(cls, asset, **kwargs)

        return self


# Sprite Factory ist in __new__ eingebaut, __new__ wird vor __init__ ausgeführt und händelt die erstellung einer instanz hingegen __init__ händelt die instanzierung von einer instanz
class Sprite:
    def __new__(cls, asset):
        asset_path = os.path.join(assets_folder, *asset.split("/"))
        self = object.__new__(Sprite)
        self.asset = asset

        self.image = pygame.image.load(asset_path).convert_alpha()
        self.image_rect = self.image.get_rect()
        return self

    def __repr__(self) -> str:
        return f"{self.asset}"


class Animation:
    pass


class Audio:
    pass


class gameObject:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.image = sprite.image
        self.image_rect = sprite.image_rect
