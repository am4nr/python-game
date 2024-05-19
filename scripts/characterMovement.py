from typing import TYPE_CHECKING

# from scripts.character import Character
if TYPE_CHECKING:
    from scripts.character import Character

class CharacterMovement:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def accelerate(self, axis, character: 'Character', mirror):
        character.acc[axis]= 0

        if mirror:
            character.acc[axis] = -character.speed
        else:
            character.acc[axis] = character.speed
        
        if character.acc[axis] != 0:
            character.acc[axis] *= 0.7071

    def execute(self, character: 'Character', mirror):
        raise NotImplementedError
        
class CharacterRun(CharacterMovement):
    def execute(self, character: 'Character', mirror):
        self.accelerate(0, character, mirror)
        character.acc.x += character.vel.x * character.friction
        character.vel.x += character.acc.x
        character.pos.x += character.vel.x + 0.5 * character.acc.x
        character.rect.x = character.pos.x


class CharacterFall(CharacterMovement):
    def execute(self, character: 'Character', mirror = False):
        self.accelerate(1, character, mirror)
        character.acc.y += character.vel.y * character.friction
        character.vel.y += character.acc.y
        character.pos.y += character.vel.y + 0.5 * character.acc.y
        character.rect.y = character.pos.y

class CharacterJump(CharacterMovement):
    def execute(self, character: 'Character', mirror = True):
        self.accelerate(1, character, mirror)
        character.acc.y += character.vel.y * character.friction
        character.vel.y += character.acc.y
        character.pos.y += character.vel.y + 0.5 * character.acc.y
        character.rect.y = character.pos.y