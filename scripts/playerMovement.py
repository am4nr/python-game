from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.character import Character

class CharacterMovement:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def accelerate(self, character: 'Character', mirror):
        character.acc_x = 0

        if mirror:
            character.acc.x = -character.speed
        else:
            character.acc.x = character.speed
        
        if character.acc.x != 0:
            character.acc.x *= 0.7071
        

class CharacterRun(CharacterMovement):
    def execute(self, character: 'Character', mirror: bool):
        self.accelerate(character, mirror)
        character.acc.x += character.vel.x * character.friction
        character.vel.x += character.acc.x
        character.pos.x += character.vel.x + 0.5 * character.acc.x
        character.rect.x = character.pos.x
