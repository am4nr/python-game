# main.py
import sys
import pygame
from scripts.flyweight import Flyweight
from scripts.settings import *
import scripts.player as player
from scripts.tiles import Tileset, Tilemap, Level
import math
import tracemalloc

class Game:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        tracemalloc.start()
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.assets = Flyweight(self)
        self.player = player.Player(
            50, 50, self.assets.get("Sprite", "characters/finn/finn_idle_alt.png")
        )
        self.clock = pygame.time.Clock()
        self.levels = [
            self.assets.get("Level", "Test-Level"),
            self.assets.get("Level", "Test-Level2"),
        ]
        self.current_level = 0

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    tracemalloc.stop()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_1]:
                        if self.current_level == 0:
                            self.current_level = len(self.levels) - 1
                        else:
                            self.current_level = self.current_level - 1
                        print(tracemalloc.get_traced_memory())
                    if keys[pygame.K_2]:
                        if self.current_level == len(self.levels) - 1:
                            self.current_level = 0
                        else:
                            self.current_level = self.current_level + 1
                        print(tracemalloc.get_traced_memory())

            self.player.update()
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            self.draw_grid()

            # temporary levelchange (später über states)

            for layer in self.levels[self.current_level].get_layers().values():
                layer["group"].draw(self.screen)

            self.screen.blit(self.player.image, self.player.rect)
            pygame.display.update()
            pygame.display.flip()

game = Game()
game.run()