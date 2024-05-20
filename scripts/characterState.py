from abc import ABCMeta, abstractmethod
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.character import Character


class CharacterState(metaclass=ABCMeta):
    def __init__(self):
        self.currentState = Idle

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    def changeState(self, character, newState):
        if (self.currentState != newState): 
            self.currentState.exit(self, character)
        self.currentState = newState
        self.currentState.enter(self, character)



class Idle(CharacterState):
    def enter(self, character: 'Character'):
        character.animation.reset(character.sprites["idle"])
    def exit(self, character: 'Character'):
        pass
    

class RunningRight(CharacterState):
    def enter(self, character: 'Character'):
        character.animation.reset(character.sprites["run"])
    def exit(self, character: 'Character'):
        self.changeState(Idle)


class RunningLeft(CharacterState):
    def enter(self, character: "Character"):
        character.animation.reset(character.animation.flip(character.sprites["run"]))
    def exit(self, character: "Character"):
        self.changeState(Idle)

class Jumping(CharacterState):
    def enter(self, character: "Character"):
        character.animation.reset(character.sprites["jump"])
    def exit(self, character: "Character"):
        self.changeState(Idle)

# class Falling(CharacterState):
#     def enter(self, character: "Character"):
#         character.animation.reset(character.sprites["jump"])
#     def exit(self, character: "Character"):
#         self.changeState(Idle)


#hit
#wallslide
#attack
#die
#powerup
#doublejump