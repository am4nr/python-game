import pygame
import os
import sys
from scripts.Level.tiles import Tilemap, Tileset

vec = pygame.math.Vector2
scripts_folders = os.path.dirname(__file__)
game_folder = os.getcwd()
assets_folder = os.path.join(game_folder, "assets")

# diese function sucht in dem Module nach Klassen mit x name damit diese später dynamisch erstellt werden
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

# flyweight als singleton damit es nur eine Instanz vom "assetmanager" gibt
class Flyweight:
    __instance = None
    collections = {}

    def __new__(cls, game):
        if cls.__instance is None:
            cls.__instance = super(Flyweight, cls).__new__(cls)
            cls.__instance.__game = game
        return cls.__instance

    def __repr__(self):
        return "\n".join("{}\t{}".format(k, v) for k, v in self.collections.items())

    # Flyweight.get prüft ob es in den collections schon die Art von Assets gibt, wenn nicht
    # wird eine neue collection dafür erstellt, wenn es diese collection schon gibt, wird geprüft,
    # ob es das asset bereits gibt, wenn nicht wird das erstellt
    # Image's sind ein special case der manuell geprüft wird sonst wird einfach die allgemeine
    # Asset Klasse benutzt um zu prüfen ob das asset erstellt oder instanziert werden muss
    def get(self, asset_type, asset, **kwargs):
        if isinstance(asset, str):
            asset_path = os.path.join(assets_folder, *asset.replace("..", "").split("/"))
        if asset_type not in self.collections:
            self.collections[asset_type] = {}

        if asset in self.collections[asset_type]:
            return self.collections[asset_type][asset]

        if asset_type == "Image":
            asset_obj = pygame.image.load(asset_path).convert_alpha()
            
        elif asset_type == "Sound":
            mixer = self.__instance.__game.sound
            asset_obj = mixer.Sound(asset_path)
            
        elif asset_type == "Music":
            mixer = self.__instance.__game.music
            mixer.load(asset_path)
            asset_obj = mixer
        else:
            asset_class = str_to_class(asset_type)
            asset_obj = asset_class(self.__game, asset, **kwargs)

        self.collections[asset_type][asset] = asset_obj
        return asset_obj
    

# Konstruktor und Initiator sind getrennt, Konstruktor setzt intrinsische values, Initiator 
# setzt extrinsische Werte und funktioniert dadurch als Factory (?)
class Asset:
    """ def __new__(cls, game, asset_type, asset, **kwargs):
        if Flyweight.collections.get(asset_type) is None:
            Flyweight.collections[asset_type] = {}
        self = Flyweight.collections.get(asset_type).get(asset)

        if self is None:
            asset_class = str_to_class(asset_type)
            self = asset_class.__new__(asset_class, game, asset)

        self.__init__(game, asset, **kwargs)
        return self """
    def __init__(self,game,asset, **kwargs):
        self.game = game
        self.asset = asset
        self.kwargs = kwargs


# Muss noch überarbeitet werden, damit der Charakter diese auch richtig benutzen kann
class Sprite(pygame.sprite.Sprite):
    def __init__(self, game, image, **kwargs):
        super().__init__()
        
        if isinstance(image, pygame.surface.Surface):
            self.image = image
        else:
            self.image = game.assets.get("Image",image)
        
        self.rect = self.image.get_rect()
        self.kwargs = kwargs
