from abc import ABCMeta, abstractmethod
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.character import Character


class CharacterState():
    def __init__(self, character):
        self.currentState = Idle
        self.character = character

    def enter(self):
        pass

    def exitState(self):
        pass

    def changeState(self, newState):
        if (self.currentState != newState): 
            self.currentState.exitState(self)
            self.currentState = newState
            self.currentState.enter(self)
        return self.currentState


class Idle(CharacterState):
    def enter(self):
        self.character.animation.get_images(self.character.sprites["idle"], False)
        
    # def exitState(self, statemachine):
    #     statemachine.changeState(Idle)
    

class RunningRight(CharacterState):
    def enter(self):
        self.character.animation.get_images(self.character.sprites["run"], False)
    # def exitState(self):
    #     self.changeState(Idle)


class RunningLeft(CharacterState):
    def enter(self):
        self.character.animation.get_images(self.character.sprites["run"], True)
    # def exitState(self):
    #     self.changeState(Idle)


class Jumping(CharacterState):
    def enter(self):
        self.character.animation.get_images(self.character.sprites["jump"], False)
    # def exitState(self):
    #     self.changeState(Idle)


# class Falling(CharacterState):
#     def enter(self, character: "Character"):
#         character.animation.get_images(character.sprites["jump"])
#     def exit(self, character: "Character"):
#         self.changeState(Idle)


#hit
#wallslide
#attack
#die
#powerup
#doublejump