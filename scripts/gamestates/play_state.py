import pygame
from scripts.gamestates.meta_state import GameState
import math
from scripts.Utils.settings import *

class PlayState(GameState):
    def enterState(self, game):
        print("Entered Playstate")
        game.music = game.assets.get("Music","music/loop.wav")
        #game.music.load("assets/music/loop.wav")
        # game.music.play(-1)

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

        game.screen.blit(game.character.image, (game.character.rect.x, game.character.rect.y - game.character.image.get_height()))
        # game.screen.blit(game.character.image, game.character.rect)