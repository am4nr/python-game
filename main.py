import sys

import pygame
from scripts.flyweight import Flyweight, Asset
from scripts.settings import *  # noqa: F403
import scripts.player as player
from scripts.tiles import Tileset, Tilemap, Level  # noqa: F401
import math


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

        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.assets = Flyweight(self)
        self.player = player.Player(self.assets.get("Sprite", "characters/finn/finn_idle_alt.png"), 50, 50, 0, 0, 0.1, 0.1, 5, 5)
        self.clock = pygame.time.Clock()
        # test_level = self.assets.get("Tilemap", "Test-Level")
        #test_level = Asset(self, "Tilemap", "Test-Level")
        #TilesetForrest = self.assets.get("Tileset", "TilesetForrest")
        TestLvl = self.assets.get("Tilemap", "Test-Level")
        TestLevel = Level(self,TestLvl)
        #print(self.assets)

    def draw_grid(self):
        for line in range(0, math.ceil(WIDTH / TILE_SIZE)):
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (0, line * TILE_SIZE),
                (WIDTH, line * TILE_SIZE),
            )
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (line * TILE_SIZE, 0),
                (line * TILE_SIZE, HEIGHT),
            )

    def run(self):
        while True:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update
            pygame.display.update()
            self.player.update()
            self.clock.tick(FPS)

            # Render

            self.screen.fill((0, 0, 0))
            self.draw_grid()

            self.screen.blit(self.player.image, self.player.rect)
            pygame.display.flip()


game = Game()
game.run()
