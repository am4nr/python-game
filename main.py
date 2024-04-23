import sys

import pygame
import scripts.utilities.flyweight as flyweight
from scripts.utilities.settings import *
import scripts.sprites.characters.main_character as main_character


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Animal Adventure")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.sprites = []
        self.player_image = flyweight.get_image_dict("characters", "finn\otter_idle_1.png")
        self.player = main_character.Entity(50, 50, 0, 0, 0, 0, self.player_image["finn\otter_idle_1.png"])
        self.clock = pygame.time.Clock()
        
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
            
Game().run()