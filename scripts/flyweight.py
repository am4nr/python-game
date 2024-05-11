import pygame
import os
import sys
from scripts.tiles import Tilemap, Tileset, Tile

# Dateisystem
scripts_folders = os.path.dirname(__file__)
game_folder = os.path.join(scripts_folders, os.pardir)
assets_folder = os.path.join(game_folder, "assets")

#helper um später in der Asset class um anhand des asset_type's die entsprechende class dafür zu suchen und zu erstellen
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

#Flyweight als singleton, damit nicht mehr als ein Flyweight erstellt werden kann -> jede Instanz von Flyweight ist die selbe
class Flyweight:
    __instance = None
    collections = {
    }

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __repr__(self):
        return "\n".join("{}\t{}".format(k, v) for k, v in self.collections.items())


class Asset:
    def __new__(cls, asset_type, asset, **kwargs):
        if Flyweight.collections.get(asset_type.lower()) == None:
            Flyweight.collections[asset_type.lower()] = {}
        self = Flyweight.collections.get(asset_type.lower()).get(asset)
        if self is None:
            self = Flyweight.collections[asset_type.lower()][asset] = str_to_class(
                asset_type
            ).__new__(cls, asset, **kwargs)
        return self


# Sprite Factory ist in __new__ eingebaut, __new__ wird vor __init__ ausgeführt und handhabt die Erstellung einer Instanz hingegen __init__ handhabt die Instanziierung von einer Instanz
class Sprite(pygame.sprite.Sprite):
    def __new__(cls, asset, x, y):
        asset_path = os.path.join(assets_folder, *asset.split("/"))
        self = object.__new__(Sprite)
        self.asset = asset

        self.image = pygame.image.load(asset_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        return self
    
    def __init__(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
    def __repr__(self) -> str:
        return f"{{asset : {self.asset}}},\n{{image: <pygame.surface>}},\n{{image_rect: <pygame.surface>}}"


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
