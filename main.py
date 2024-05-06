import sys
import pygame
from scripts.flyweight import Flyweight, Asset
from scripts.settings import *
import scripts.main_character as main_character
from scripts.tiles import Tileset, Tilemap


class Game:
    __instance = None

    def __new__(
        cls,
    ):  # Game soll singleton sein, damit es sich immer um die selbe Instanz von Game handelt
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Animal Adventure")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.sprites = []
        self.player = main_character.Entity(
            50, 50, 0, 0, 0, 0, Asset("Sprite", "characters/finn/finn_idle.png")
        )
        self.clock = pygame.time.Clock()
        self.flyweight = Flyweight()
        terrain = Asset("Tileset", "terrain")

        print(self.flyweight)

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


game = Game()
game.run()
