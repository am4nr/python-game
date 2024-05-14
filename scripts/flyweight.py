import pygame
import os
import sys
from scripts.tiles import Tilemap, Tileset, Level
from scripts.main_character import Entity

# Dateisystem
scripts_folders = os.path.dirname(__file__)
game_folder = os.path.join(scripts_folders, os.pardir)
assets_folder = os.path.join(game_folder, "assets")


# helper um später in der Asset class um anhand des asset_type's die entsprechende class dafür zu suchen und zu erstellen
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


# Flyweight als singleton, damit nicht mehr als ein Flyweight erstellt werden kann -> jede Instanz von Flyweight ist die selbe
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
            return asset

        if asset_type == "Image":
            self.collections[asset_type][asset] = pygame.image.load(
                os.path.join(assets_folder, *asset.replace("..", "").split("/"))
            )
            return self.collections[asset_type][asset]

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
            self = Flyweight.collections[asset_type][asset] = str_to_class(
                asset_type
            ).__new__(cls, game, asset)

        self.__init__(**kwargs)
        return self


# Sprite Factory ist in __new__ eingebaut, __new__ wird vor __init__ ausgeführt und handhabt die Erstellung einer Instanz hingegen __init__ handhabt die Instanziierung von einer Instanz
class Sprite(pygame.sprite.Sprite):
    def __new__(cls, game, asset, **kwargs):
        self = object.__new__(Sprite)
        self.asset_path = os.path.join(assets_folder, *asset.split("/"))
        self.asset = asset

        self.image = game.assets.get("Image", asset)
        self.rect = self.image.get_rect()
        return self

    def __init__(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def __repr__(self) -> str:
        return f"{{asset : {self.asset}}},\n{{image: <pygame.surface>}},\n{{image_rect: <pygame.surface>}}"

