import sys

import pygame
import scripts.utilities.flyweight as flyweight
from scripts.utilities.settings import *
import scripts.sprites.characters.main_character as main_character
from scripts.sprites.tiles import Tileset, Tilemap


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Animal Adventure")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.sprites = []
        self.player_image = flyweight.get_image_dict("characters", "finn\/finn_idle.png")
        self.player = main_character.Entity(50, 50, 0, 0, 0, 0, self.player_image["finn\/finn_idle.png"])
        self.clock = pygame.time.Clock()
        self.assets = {"tilesets":[],"maps":[]}
        
        morning_adventure = Tileset("morning_adventure", self)
        testmap = Tilemap("Test-Level", self)
        
        print(self.assets)
        
    def assetmanager(self, type, asset):
        if type == "tileset" or type == "map":
            self.assets[type+"s"].append(asset) 
            
    def run(self):
        while True:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Update
            pygame.display.update()
            self.clock.tick(FPS)

            # Render
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.player.image, self.player.image_rect)

            pygame.display.flip()
            
game = Game()
game.run()