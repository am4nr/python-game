from abc import ABCMeta, abstractmethod
import pygame
from scripts.Utils.settings import *
from scripts.Character.characterMovement import HorizontalMovement, VerticalMovement

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from scripts.Character.character import Character


class CharacterState():
    def __init__(self, character):
        self.currentState = Idle
        self.character = character

    def enter(self):
        pass

    def update(self):
        self.currentState.update(self)
        

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
        self.character.animation.reset(self.character.sprites["idle"], self.character.direction)
        self.character.rect.update(self.character.pos, self.character.image.get_size())

    def update(self):
        pass

    def exitState(self):
        pass
    

class RunningRight(CharacterState):
    def enter(self):
        self.character.vel.x = 0
        self.character.direction = "right"
        if self.character.on_ground:
            self.character.animation.reset(
                self.character.sprites["run"], self.character.direction
            )
            self.character.rect.update(self.character.pos, self.character.image.get_size())

    def update(self):
        HorizontalMovement().execute(self.character)


    def exitState(self):
        self.character.vel.x = 0


class RunningLeft(CharacterState):
    def enter(self):
        self.character.vel.x = 0
        self.character.direction = "left"
        if self.character.on_ground:
            self.character.animation.reset(
                self.character.sprites["run"], self.character.direction
            )
            self.character.rect.update(self.character.pos, self.character.image.get_size())

    def update(self):
        HorizontalMovement().execute(self.character)


    def exitState(self):
        self.character.vel.x = 0


class Jumping(CharacterState):
    def enter(self):
        self.character.jumping = True
        self.character.vel.y = -GRAVITY * 22
        self.character.jumps -= 1
        self.character.animation.reset(self.character.sprites["jump"], self.character.direction, False, 6)
        self.character.sounds_jump.play()
        self.character.rect.update(self.character.pos, self.character.image.get_size())

    def update(self):
        VerticalMovement().execute(self.character)
        if self.character.animation.check_done():
            self.character.state.changeState(Falling)

    def exitState(self):
        self.character.vel.y = 0
        self.character.jumping = False
        self.changeState


class Falling(CharacterState):
    def enter(self):
        # self.character.jumping = False
        self.character.vel.y = GRAVITY
        self.character.animation.reset(self.character.sprites["fall"], self.character.direction)
        
        self.character.rect.update(self.character.pos, self.character.image.get_size())

    def update(self):
        if not self.character.on_ground:
            VerticalMovement().execute(self.character)
        else: 
            self.character.state.changeState(Landing)

    def exitState(self):
        self.character.vel.y =0


class Landing(CharacterState):
    def enter(self):
        self.character.animation.reset(self.character.sprites["land"], self.character.direction, False)
        self.character.rect.update(self.character.pos, self.character.image.get_size())
        
    def update(self):
        if self.character.animation.check_done():
            self.character.state.changeState(Idle)
    def exitState(self):
        pass
        


#hit
#wallslide
#attack
#die
#powerup
#doublejump