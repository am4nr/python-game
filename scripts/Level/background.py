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
        self.offset_multiplier = {"sky": 0, "bg_decor": 0.25, "mid_decor": .5, "fg_decor": .75, "ground": 1}
        
    def load(self, game):
        self.game = game
        self.sky = self.game.assets.get("Image",self.file_prefix+"Sky"+self.file_suffix)
        self.bg_decor = self.game.assets.get("Image",self.file_prefix+"BG_Decor"+self.file_suffix)
        self.mid_decor = self.game.assets.get("Image",self.file_prefix+"Middle_Decor"+self.file_suffix)
        self.fg_decor = self.game.assets.get("Image",self.file_prefix+"Foreground"+self.file_suffix)
        self.ground = self.game.assets.get("Image",self.file_prefix+"Ground"+self.file_suffix)
        
    def update(self):
        self.offset_x = self.game.level_manager.current_level.offset_x
        self.offset_y = self.game.level_manager.current_level.offset_y
        
    def draw(self):
        sky = pygame.transform.scale(self.sky, (self.sky.get_width()*0.8, HEIGHT))
        bg_decor = pygame.transform.scale(self.bg_decor, (self.bg_decor.get_width()*0.8, HEIGHT))
        mid_decor = pygame.transform.scale(self.mid_decor, (self.mid_decor.get_width()*0.8, HEIGHT))
        fg_decor = pygame.transform.scale(self.fg_decor, (self.fg_decor.get_width()*0.8, HEIGHT))
        
        sky_width = sky.get_width()
        bg_decor_width = bg_decor.get_width()
        mid_decor_width = mid_decor.get_width()
        fg_decor_width = fg_decor.get_width()
        ground_width = self.ground.get_width()

        sky_offset = -math.floor(self.offset_x * self.offset_multiplier["sky"]) % sky_width
        bg_decor_offset = -math.floor(self.offset_x * self.offset_multiplier["bg_decor"]) % bg_decor_width
        mid_decor_offset = -math.floor(self.offset_x * self.offset_multiplier["mid_decor"]) % mid_decor_width
        fg_decor_offset = -math.floor(self.offset_x * self.offset_multiplier["fg_decor"]) % fg_decor_width
        ground_offset = -math.floor(self.offset_x * self.offset_multiplier["ground"]) % ground_width

        self.game.screen.blit(sky, (sky_offset, 0))
        self.game.screen.blit(sky, (sky_offset - sky_width, 0))
        self.game.screen.blit(bg_decor, (bg_decor_offset, 0))
        self.game.screen.blit(bg_decor, (bg_decor_offset - bg_decor_width, 0))
        self.game.screen.blit(mid_decor, (mid_decor_offset, 0))
        self.game.screen.blit(mid_decor, (mid_decor_offset - mid_decor_width, 0))
        self.game.screen.blit(fg_decor, (fg_decor_offset, 0))
        self.game.screen.blit(fg_decor, (fg_decor_offset - fg_decor_width, 0))
        self.game.screen.blit(self.ground, (ground_offset, 0))
        self.game.screen.blit(self.ground, (ground_offset - ground_width, 0))