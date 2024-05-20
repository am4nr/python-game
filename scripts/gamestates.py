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
    def enterState(self, game):




# den Abschnitt hier noch bearbeiten (bis siehe unteren Kommentar)

import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((800, 640))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/background/BG.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(320, 130))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(320, 230), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(320, 130))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(320, 230), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(320, 50))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/XXXXXXXXXX"), pos=(320, 125), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/XXXXXXXXXX"), pos=(320, 200), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/XXXXXXXXXX"), pos=(320, 275), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()



# bis hier den Abschnitt bearbeiten

    
   











    def exitState(self, game):
        pass

    def event(self, game, event):
        pass

    def update(self, game):
        pass

    def render(self, game):
        game.screen.fill((255, 255, 255))

















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
        ]
        self.current_level = 0
        # print(tracemalloc.get_traced_memory())
        self.state = MainMenuState()

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
        self.clock.tick(FPS)

    def render(self):
        self.state.render(self)
        pygame.display.update()
        pygame.display.flip()

    def run(self):
        while True:
            self.event()
            self.update()
            self.render()
