from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.character import Character
from scripts.characterState import RunningLeft, RunningRight, Jumping
from scripts.characterMovement import HorizontalMovement, VerticalMovement


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
        character.state.changeState(RunningLeft)
        HorizontalMovement().execute(character, left=True)

class RunRight(PlayerCommand):
    def execute(self, character: 'Character'):
        character.state.changeState(RunningRight)
        HorizontalMovement().execute(character, right=True)

class Jump(PlayerCommand):
    def execute(self, character: 'Character'):
        character.state.changeState(Jumping)
        VerticalMovement().execute(character)
        
class Attack(PlayerCommand):
    def execute(self, character: 'Character'):
        pass

class Dash(PlayerCommand):
    pass

class Duck(PlayerCommand):
    pass