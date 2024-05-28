from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.Character.character import Character
from scripts.Character.characterState import Run, inAir
from scripts.Character.characterMovement import HorizontalMovement, VerticalMovement
from scripts.Utils.settings import *


class PlayerCommand():
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    def execute(self, character: 'Character'):
        raise NotImplementedError

class RunLeft(PlayerCommand):
    def execute(self, character: 'Character'):
        character.direction = "left"
        character.state.changeState(Run)
        HorizontalMovement().execute(character)

class RunRight(PlayerCommand):
    def execute(self, character: 'Character'):
        character.direction = "right"
        character.state.changeState(Run)
        HorizontalMovement().execute(character)

class Jump(PlayerCommand):
    def execute(self, character: 'Character'):
        # if character.jumps>0:
        character.jumping = True
        character.jumps -= 1
        character.vel.y = -GRAVITY * 60
        character.state.changeState(inAir)
        VerticalMovement().execute(character)
        
class Attack(PlayerCommand):
    def execute(self, character: 'Character'):
        pass

class Dash(PlayerCommand):
    pass

class Duck(PlayerCommand):
    pass