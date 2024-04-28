import pygame
import os

# Dateisystem
utilities_folder = os.path.dirname(__file__)
scripts_folder = os.path.join(utilities_folder, os.pardir)
game_folder = os.path.join(scripts_folder, os.pardir)


def get_image_dict(asset_category, asset_name):
    image_dict = {}
    image_dict[asset_name] = pygame.image.load(os.path.join(game_folder, "assets", asset_category, asset_name)).convert_alpha()
    return image_dict

# to do: def get_tiles_dict()