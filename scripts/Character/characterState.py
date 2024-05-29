from abc import ABCMeta, abstractmethod
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.Character.character import Character


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
        self.character.animation.get_images(self.character.sprites["idle"], self.character.direction)
        # self.character.rect.update(self.character.pos, self.character.image.get_size())

    # def exitState(self, statemachine):
    #     statemachine.changeState(Idle)
    

class RunningRight(CharacterState):
    def enter(self):
        self.character.animation.get_images(
            self.character.sprites["run"], self.character.direction
        )
        # self.character.rect.update(self.character.pos, self.character.image.get_size())


#     # def exitState(self):
#     #     self.changeState(Idle)


class RunningLeft(CharacterState):
    def enter(self):
        self.character.animation.get_images(
            self.character.sprites["run"], self.character.direction
        )
        # self.character.rect.update(self.character.pos, self.character.image.get_size())


#     # def exitState(self):
#     #     self.changeState(Idle)


class Jumping(CharacterState):
    def enter(self):
        self.character.animation.get_images(self.character.sprites["jump"], self.character.direction)
        self.character.sounds_jump.play()
        # self.character.rect.update(self.character.pos, self.character.image.get_size())

    # def exitState(self):
    #     self.changeState(Land)

class Falling(CharacterState):
    def enter(self):
        self.character.animation.get_images(self.character.sprites["jump"], self.character.direction)
        
        # self.character.rect.update(self.character.pos, self.character.image.get_size())

    # def exitState(self):
    #     self.changeState(Land)


class Landing(CharacterState):
    def enter(self):
        self.character.animation.get_images(self.character.sprites["land"], self.character.direction)
        # self.character.rect.update(self.character.pos, self.character.image.get_size())
        
    # def exitState(self):
    #     self.changeState(Land)



#hit
#wallslide
#attack
#die
#powerup
#doublejump