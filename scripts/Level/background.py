import pygame

class Background:
    def __init__(self, game, level_number):
        self.game = game
        self.file_prefix = "assets/background/"
        self.file_suffix = "_0"+level_number+".png"
        self.sky = self.game.assets.get("Image",self.file_prefix+"Sky"+self.file_suffix)
        self.bg_decor = self.game.assets.get("Image",self.file_prefix+"BG_Decor"+self.file_suffix)
        self.mid_decor = self.game.assets.get("Image",self.file_prefix+"Middle_Decor"+self.file_suffix)
        self.fg_decor = self.game.assets.get("Image",self.file_prefix+"Foreground"+self.file_suffix)
        self.ground = self.game.assets.get("Image",self.file_prefix+"Ground"+self.file_suffix)
        print(f"Loaded Background for level {level_number}")
        print(self.sky), print(self.bg_decor), print(self.mid_decor), print(self.fg_decor), print(self.ground)
        
    def draw(self):
        self.game.screen.blit(self.sky, (0,0))
        self.game.screen.blit(self.bg_decor, (0,0))
        self.game.screen.blit(self.mid_decor, (0,0))
        self.game.screen.blit(self.fg_decor, (0,0))
        self.game.screen.blit(self.ground, (0,0))