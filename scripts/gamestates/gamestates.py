import pygame
import sys

from pygame import mixer

from scripts.Utils.settings import *
from scripts.Utils.flyweight import Flyweight

from scripts.Character.character import Character
from scripts.Utils.spritesheetManager import SpritesheetManager


from scripts.gamestates.play_state import PlayState
from scripts.gamestates.main_menu_state import MainMenuState
from scripts.gamestates.options_state import OptionsState
from scripts.gamestates.game_over_state import GameOverState

from scripts.Level.levels import LevelManager


class Game:
    def __init__(self):
        self.audio_volume = 0.6
        pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()
        self.sound = pygame.mixer
        self.music = pygame.mixer.music

        pygame.init()

        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.assets = Flyweight(self)
        self.sprites = SpritesheetManager(self.assets)
        self.states = {
            "Play": PlayState(),
            "MainMenu": MainMenuState(),
            "Options": OptionsState(),
            "GameOver": GameOverState(),
        }

        self.mouse_pos = pygame.mouse.get_pos()
        self.keystate = pygame.key.get_pressed()
        self.events = None

        self.level_manager = LevelManager(self)
        self.level_manager.set_level("Test-Level")

        self.clock = pygame.time.Clock()

        self.state = None
        self.changeState(MainMenuState())
        self.previousState = None

    def changeState(self, newState):
        self.previousState = self.state
        self.state = newState
        self.state.enterState(self)

    def event(self):
        self.events = pygame.event.get()
        for event in self.events:
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
            if isinstance(self.state, PlayState):
                self.level_manager.current_level.check_goal()
