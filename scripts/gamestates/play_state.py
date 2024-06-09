import pygame
from scripts.gamestates.meta_state import GameState
import math
from scripts.Utils.settings import *

class PlayState(GameState):
    def enterState(self, game):
        print("Entered Playstate")
        game.music = game.assets.get("Music","music/loop.wav")
        if game.previousState == game.states["MainMenu"]:
            game.level_manager.current_level.load()
        #game.music.load("assets/music/loop.wav")
        #game.music.play(-1)

    def exitState(self, game):
        pass

    def event(self, game, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                game.changeState(game.states["Options"])
            if keys[pygame.K_2]:
                game.level_manager.next_level()

    def update(self, game):
        #print("Updating play state")
        game.level_manager.current_level.update()
        #print("Updated current level")
    

    def render(self, game):
        #print("Rendering play state")
        game.screen.fill((0, 0, 0))
        # for line in range(0, math.ceil(WIDTH / TILE_SIZE)):
        #     pygame.draw.line(
        #         game.screen,
        #         (255, 255, 255),
        #         (0, line * TILE_SIZE),
        #         (WIDTH, line * TILE_SIZE),
        #     )
        #     pygame.draw.line(
        #         game.screen,
        #         (255, 255, 255),
        #         (line * TILE_SIZE, 0),
        #         (line * TILE_SIZE, HEIGHT),
        #     )
            
        game.level_manager.current_level.render()
        #print("Rendered current level")
        # game.screen.blit(game.character.image, game.character.rect)