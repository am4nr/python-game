# flyweight.py
import pygame
import os
import sys
from scripts.tiles import Tilemap, Tileset, Level

scripts_folders = os.path.dirname(__file__)
game_folder = os.path.join(scripts_folders, os.pardir)
assets_folder = os.path.join(game_folder, "assets")

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

class Flyweight:
    __instance = None
    collections = {}

    def __new__(cls, game):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, game):
        self.game = game

    def __repr__(self):
        return "\n".join("{}\t{}".format(k, v) for k, v in self.collections.items())

    def get(self, asset_type, asset, **kwargs):
        if asset_type not in self.collections:
            self.collections[asset_type] = {}

        if asset in self.collections[asset_type]:
            return self.collections[asset_type][asset]

        if asset_type == "Image":
            self.collections[asset_type][asset] = pygame.image.load(
                os.path.join(assets_folder, *asset.replace("..", "").split("/"))
            ).convert_alpha()
            return self.collections[asset_type][asset]

        if asset_type == "Sprite":
            sprite_image = self.get("Image", asset)
            return Sprite(self.game, sprite_image)

        self.collections[asset_type][asset] = Asset(
            self.game, asset_type, asset, **kwargs
        )
        return self.collections[asset_type][asset]

class Asset:
    def __new__(cls, game, asset_type, asset, **kwargs):
        if Flyweight.collections.get(asset_type) is None:
            Flyweight.collections[asset_type] = {}
        self = Flyweight.collections.get(asset_type).get(asset)

        if self is None:
            asset_class = str_to_class(asset_type)
            self = asset_class.__new__(asset_class, game, asset)

        self.__init__(game, asset, **kwargs)
        return self

# Sprite Factory
class Sprite(pygame.sprite.Sprite):
    def __new__(cls, game, image, **kwargs):
        self = object.__new__(Sprite)
        self.image = image
        self.rect = self.image.get_rect()
        return self

    def __init__(self, game, image, **kwargs):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
