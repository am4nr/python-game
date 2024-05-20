from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.character import Character

class Movement:
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
        
class HorizontalMovement(Movement):
    def execute(self, character: 'Character', mirror):
        self.accelerate(0, character, mirror)
        character.acc.x += character.vel.x * character.friction
        character.vel.x += character.acc.x
        character.pos.x += character.vel.x + 0.5 * character.acc.x
        character.rect.x = character.pos.x


class VerticalMovement(Movement):
    def execute(self, character: 'Character', mirror):
        self.accelerate(1, character, mirror)
        character.acc.y += character.vel.y * character.friction
        character.vel.y += character.acc.y
        character.pos.y += character.vel.y + 0.5 * character.acc.y
        character.rect.bottom = character.pos.y