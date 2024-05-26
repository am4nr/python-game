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
from scripts.button import Button


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
    buttons = {}
    def enterState(self, game):
        self.buttons["PLAY_BACK"] = Button(image=None, pos=(320, 230), 
                                text_input="BACK", font=self.get_font(75), base_color="White", hovering_color="Green")
        
        self.buttons["OPTIONS_BACK"] = Button(image=None, pos=(320, 230), 
                            text_input="BACK", font=self.get_font(75), base_color="Black", hovering_color="Green")
        
        self.buttons["PLAY_BUTTON"] = Button(game.assets.get("Image","objects/buttons/play_button.png"), pos=(320, 125), 
                                text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.buttons["OPTIONS_BUTTON"] = Button(game.assets.get("Image","objects/buttons/play_button.png"), pos=(320, 200), 
                                text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.buttons["QUIT_BUTTON"] = Button(game.assets.get("Image","objects/buttons/cancel_button.png"), pos=(320, 275), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

        #main_menu()

# für jeden screen ein gamestate (also jede szene, zb play, options, und für quit brauchen wir kein extra state)

    def get_bg(self, game):
        return game.assets.get("Image", "background/BG.png")

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        #font fehlt in asset ordner
        return pygame.font.Font("assets/font/Pacifico.ttf", size)

    def play(self,game):
        game.changeState(PlayState())
        
    def options(self, game):
        game.changeState(OptionsState())
            
    def main_menu(self, game):
        pass             

    def exitState(self, game):
        pass

    def event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons["PLAY_BACK"].checkForInput(game.mousepos):
                self.main_menu(game)
        
        #event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons["OPTIONS_BACK"].checkForInput(game.mousepos):
                self.main_menu()

    # der part kommt in die event methode (mainmenu.event())
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons["PLAY_BUTTON"].checkForInput(game.mousepos):
                self.play(game)
            if self.buttons["OPTIONS_BUTTON"].checkForInput(game.mousepos):
                self.options(game)
            if self.buttons["QUIT_BUTTON"].checkForInput(game.mousepos):
                pygame.quit()
                sys.exit()

    def update(self, game):
        pass

    def render(self, game):
        game.screen.fill((255, 255, 255))

        PLAY_TEXT = self.get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(320, 130))
        game.screen.blit(PLAY_TEXT, PLAY_RECT)

        
        
        self.buttons["PLAY_BACK"].changeColor(game.mousepos)
        self.buttons["PLAY_BACK"].update(game.screen)

#render game.screen = game.screen
        game.screen.fill("white")

        OPTIONS_TEXT = self.get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(320, 130))
        game.screen.blit(OPTIONS_TEXT, OPTIONS_RECT)


        self.buttons["OPTIONS_BACK"].changeColor(game.mousepos)
        self.buttons["OPTIONS_BACK"].update(game.screen)

        #der part kommt in die render methode (mainmenu.render())
        BG=self.get_bg(game)
        game.screen.blit(BG, (0, 0))

        MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(320, 50))

        
        game.screen.blit(MENU_TEXT, MENU_RECT)

        for button in [self.buttons["PLAY_BUTTON"], self.buttons["OPTIONS_BUTTON"], self.buttons["QUIT_BUTTON"]]:
            button.changeColor(game.mousepos)
            button.update(game.screen)        


class OptionsState(GameState):
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
            #print(f"rendered layer: {layer}")
            layer["group"].draw(game.screen)

        print(tracemalloc.get_traced_memory())
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
        self.mousepos = None
        tracemalloc.start()
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.assets = Flyweight(self)
        self.sprites = CharacterSpriteManager(self.assets)
        self.state = PlayState()

        self.levels = [
            self.assets.get("Tilemap", "Test-Level"),
            self.assets.get("Tilemap", "Test-Level2"),
        ]
        self.current_level = 0
        
        self.character_sprites = self.sprites.handle_spritesheetDictTransformation(
            self.sprites.get_spritesheets("characters", "finn"),
            200,
            200,
            0.32,
        )
        self.character = Character(self, self.character_sprites, 0.75, -0.12)
        self.clock = pygame.time.Clock()

        # print(tracemalloc.get_traced_memory())
        # print(tracemalloc.get_traced_memory())
        self.state = None
        self.changeState(MainMenuState())

    def changeState(self, newState):
    #    self.state.exitState(self)
        self.state = newState
        self.state.enterState(self)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                tracemalloc.stop()
                sys.exit()
            self.state.event(self, event)

    def update(self):
        self.mousepos=pygame.mouse.get_pos()  
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
