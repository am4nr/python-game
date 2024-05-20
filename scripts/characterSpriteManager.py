import pygame
import os
from pathlib import Path
from scripts.flyweight import *
class CharacterSpriteManager:
    def __init__(self, assetmanager):
        self.assetmanager = assetmanager

    def get_spritesheets(self, folder):
        self.path = os.path.join(os.getcwd(), "assets", folder)
        self.spritesheets = {}
        for filename in os.listdir(self.path):
            self.spritesheets[filename.split('.')[0]] = self.assetmanager.get('Image', folder + filename)
        return self.spritesheets
    
    def handle_spritesheetDictTransformation(self, spritesheets, width, height, factor = 1):
        self.spritelists = {}
        for  key, value in spritesheets.items():
            self.spritelists[key] = self.get_sprites(value, width, height, factor)
        return self.spritelists

    def get_sprites(self, spritesheet, width, height, factor = 1):
        self.sprites = []
        for i in range(spritesheet.get_width() // width):
            surface = pygame.Surface((width,height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(spritesheet, (0,0), rect)
            print(type(pygame.transform.scale_by(surface,factor)))
            sprite = self.assetmanager.get("Sprite", pygame.transform.scale_by(surface, factor))
            self.sprites.append(sprite)
            
        return self.sprites
