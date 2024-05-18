import sys
import pygame
from scripts.flyweight import Flyweight
from scripts.settings import *  # noqa: F403
from scripts.character import Character
from scripts.tiles import Tileset, Tilemap, Level  # noqa: F401
import math
from scripts.characterSpriteManager import CharacterSpriteManager


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
        self.sprites = CharacterSpriteManager()
        self.character_sprites = self.sprites.handle_spritesheetDictTransformation(self.sprites.get_spritesheets(self.assets, "characters/finn/", "Sprite"), 200, 200, 0.32)
        self.character = Character(self.character_sprites, 0.75, -0.12)

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
            self.character.update()
            self.clock.tick(FPS)

            # Render

            self.screen.fill((0, 0, 0))
            self.draw_grid()

            self.screen.blit(self.character.image, self.character.rect)
            pygame.display.flip()


game = Game()
game.run()
