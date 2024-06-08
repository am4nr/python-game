# This file contains the Background class which is responsible for loading and drawing the background images for the level
import pygame
import math
from scripts.Utils.settings import HEIGHT
class Background:
    def __init__(self, level_number):
        self.game = None
        self.file_prefix = "background/"
        self.level_number = level_number
        self.file_suffix = "_0"+level_number+".png"
        self.offset = 0
        self.offset_multiplier = {"sky": 0.5, "bg_decor": 0.75, "mid_decor": 1, "fg_decor": 1.25, "ground": 1.5}
        
    def load(self, game):
        self.game = game
        self.sky = self.game.assets.get("Image",self.file_prefix+"Sky"+self.file_suffix)
        self.bg_decor = self.game.assets.get("Image",self.file_prefix+"BG_Decor"+self.file_suffix)
        self.mid_decor = self.game.assets.get("Image",self.file_prefix+"Middle_Decor"+self.file_suffix)
        self.fg_decor = self.game.assets.get("Image",self.file_prefix+"Foreground"+self.file_suffix)
        self.ground = self.game.assets.get("Image",self.file_prefix+"Ground"+self.file_suffix)
        print(f"Loaded Background for level {self.level_number}")
        print(self.sky), print(self.bg_decor), print(self.mid_decor), print(self.fg_decor), print(self.ground)
        
    def update(self):
        self.offset = self.game.level_manager.current_level.offset
        
    def draw(self):
        sky = pygame.transform.scale(self.sky, (self.sky.get_width()*0.8, HEIGHT))
        bg_decor = pygame.transform.scale(self.bg_decor, (self.bg_decor.get_width()*0.8, HEIGHT))
        mid_decor = pygame.transform.scale(self.mid_decor, (self.mid_decor.get_width()*0.8, HEIGHT))
        fg_decor = pygame.transform.scale(self.fg_decor, (self.fg_decor.get_width()*0.8, HEIGHT))
        
        self.game.screen.blit(sky, (math.floor(self.offset*self.offset_multiplier["sky"]), 0))
        self.game.screen.blit(sky, (math.floor(self.offset*self.offset_multiplier["sky"])-sky.get_width(), 0))
        self.game.screen.blit(bg_decor, (math.floor(self.offset*self.offset_multiplier["bg_decor"]), 0))
        self.game.screen.blit(bg_decor, (math.floor(self.offset*self.offset_multiplier["bg_decor"])-bg_decor.get_width(), 0))
        self.game.screen.blit(mid_decor, (math.floor(self.offset*self.offset_multiplier["mid_decor"]), 0))
        self.game.screen.blit(mid_decor, (math.floor(self.offset*self.offset_multiplier["mid_decor"])-mid_decor.get_width(), 0))
        self.game.screen.blit(fg_decor, (math.floor(self.offset*self.offset_multiplier["fg_decor"]), 0))
        self.game.screen.blit(fg_decor, (math.floor(self.offset*self.offset_multiplier["fg_decor"])-fg_decor.get_width(), 0))
        self.game.screen.blit(self.ground, (math.floor(self.offset*self.offset_multiplier["ground"]), 0))
