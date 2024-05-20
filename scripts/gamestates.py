from abc import ABCMeta, abstractmethod
import sys
import pygame
from scripts.flyweight import Flyweight
from scripts.settings import *
from scripts.character import Character
from scripts.characterSpriteManager import CharacterSpriteManager
from scripts.tiles import Tileset, Tilemap, Level
import math
import tracemalloc


class GameState(metaclass=ABCMeta):
    @abstractmethod
    def enterState(self):
        pass

    @abstractmethod
    def exitState(self):
        pass

    @abstractmethod
    def event(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass


class MainMenuState(GameState):
    def enterState(self):
        pass

    def exitState(self):
        pass

    def event(self):
        pass

    def update(self):
        pass

    def render(self):
        pass


class PlayState(GameState):
    def enterState(self, game):
        pass

    def exitState(self, game):
        pass

    def event(self, game, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                if game.current_level == 0:
                    game.current_level = len(game.levels) - 1
                else:
                    game.current_level = game.current_level - 1
            if keys[pygame.K_2]:
                if game.current_level == len(game.levels) - 1:
                    game.current_level = 0
                else:
                    game.current_level = game.current_level + 1

    def update(self, game):
        game.character.update()
        game.clock.tick(FPS)

    def render(self, game):
        game.screen.fill((0, 0, 0))
        for line in range(0, math.ceil(WIDTH / TILE_SIZE)):
            pygame.draw.line(
                game.screen,
                (255, 255, 255),
                (0, line * TILE_SIZE),
                (WIDTH, line * TILE_SIZE),
            )
            pygame.draw.line(
                game.screen,
                (255, 255, 255),
                (line * TILE_SIZE, 0),
                (line * TILE_SIZE, HEIGHT),
            )
        for layer in game.levels[game.current_level].get_layers().values():
            layer["group"].draw(game.screen)

        # print(tracemalloc.get_traced_memory())
        game.screen.blit(game.character.image, game.character.rect)


class GameOver(GameState):
    def enterState(self):
        pass

    def exitState(self):
        pass

    def event(self):
        pass

    def update(self):
        pass

    def render(self):
        pass


class Game:
    def __init__(self):
        tracemalloc.start()
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.assets = Flyweight(self)
        self.sprites = CharacterSpriteManager(self.assets)
        self.character_sprites = self.sprites.handle_spritesheetDictTransformation(
            self.sprites.get_spritesheets("characters/finn/"),
            200,
            200,
            0.32,
        )
        self.character = Character(self.character_sprites, 0.75, -0.12)
        self.clock = pygame.time.Clock()

        # print(tracemalloc.get_traced_memory())

        self.levels = [
            self.assets.get("Tilemap", "Test-Level"),
            self.assets.get("Tilemap", "Test-Level2"),
            self.assets.get("Tilemap", "Level2"),
        ]
        self.current_level = 0
        # print(tracemalloc.get_traced_memory())
        self.state = PlayState()

    def changeState(self, newState):
        self.state = newState

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                tracemalloc.stop()
                sys.exit()
            self.state.event(self, event)

    def update(self):
        self.state.update(self)

    def render(self):
        self.state.render(self)
        pygame.display.update()
        pygame.display.flip()

    def run(self):
        while True:
            self.event()
            self.update()
            self.render()
