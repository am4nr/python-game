from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.character import Character
from scripts.playerMovement import CharacterRun
import pygame
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
        # move char
        CharacterRun().execute(character, True)
        # render image
        flippedSprites = []
        for sprite in character.sprites["run"]:
           flippedSprites.append(pygame.transform.flip(sprite, True, False))
        character.animation.get_image(flippedSprites)

class RunRight(PlayerCommand):
    def execute(self, character: 'Character'):
        # move char
        CharacterRun().execute(character,  False)
        # render image
        character.animation.get_image(character.sprites["run"])

class Jump(PlayerCommand):
    def execute(self, character: 'Character'):
        pass

class Attack(PlayerCommand):
    def execute(self, character: 'Character'):
        pass