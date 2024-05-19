from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.character import Character
from scripts.characterState import RunningLeft, RunningRight
from scripts.characterMovement import CharacterRun, CharacterJump


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
        CharacterRun().execute(character, True)


class RunRight(PlayerCommand):
    def execute(self, character: 'Character'):
        character.state.changeState(RunningRight)
        CharacterRun().execute(character, False)


# class Jump(PlayerCommand):
#     def execute(self, character: 'Character'):
#         CharacterJump().execute(character, True)
#         character.animation.get_image(character.sprites["jump"])

# class Attack(PlayerCommand):
#     def execute(self, character: 'Character'):
#         pass