import pygame
import sys

from pygame import mixer

from scripts.Utils.settings import *
from scripts.Utils.flyweight import Flyweight

from scripts.Character.character import Character
from scripts.Character.characterSpriteManager import CharacterSpriteManager


from scripts.gamestates.play_state import PlayState
from scripts.gamestates.main_menu_state import MainMenuState
from scripts.gamestates.options_state import OptionsState


from scripts.Level.levels import LevelManager
class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()
        self.sound = pygame.mixer
        self.music = pygame.mixer.music
        pygame.init()
        
        
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.assets = Flyweight(self)
        self.sprites = CharacterSpriteManager(self.assets)
        self.states = {
            "Play":PlayState(),
            "MainMenu": MainMenuState(),
            "Options": OptionsState(),
            }

        self.mouse_pos = pygame.mouse.get_pos()
        self.keystate = pygame.key.get_pressed()

        self.level_manager = LevelManager(self)
        self.level_manager.set_level("Test-Level")

        self.character_sprites = self.sprites.handle_spritesheetDictTransformation(
            self.sprites.get_spritesheets("characters", "finn"),
            200,
            200,
            0.32,
        )
        self.character = Character(self, self.character_sprites, 0.75, -0.12)
        self.clock = pygame.time.Clock()
        
        self.state = None
        self.changeState(MainMenuState())

    def changeState(self, newState):
        #self.state.exitState(self)
        self.state = newState
        self.state.enterState(self)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.state.event(self, event)

    def update(self):
        self.keystate = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
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
