import sys
import pygame
import utilities.flyweight as flyweight
#from utilities.spritesheet import CharacterSpritesheet
from utilities.settings import *
import scripts.player as player


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Animal Adventure")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.sprites = []
        self.player_image = flyweight.get_image_dict("characters", "finn", "finn_idle_alt.png")
        self.player = player.Entity(50, 50, 50, 50, 0, 0, 0, 0,self.player_image["finn_idle_alt.png"])
        self.clock = pygame.time.Clock()
        # self.character_spritesheet = CharacterSpritesheet("finn", "finn_idle_alt.png")
        
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
            self.screen.blit(self.player.image, self.player.rect)

            pygame.display.flip()
            
Game().run()