from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.character import Character

class Movement:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def accelerate(self, axis, character: 'Character'):
        character.acc[axis] = 0
        
        if character.direction == "left":
            character.acc[axis] = -character.speed
        elif character.direction == "right":
            character.acc[axis] = character.speed
        
        if character.acc[axis] != 0:
            character.acc[axis] *= 0.7071

    def execute(self, character: 'Character'):
        raise NotImplementedError
        
class HorizontalMovement(Movement):
    def execute(self, character: 'Character', **kwargs):
        left = kwargs.get("left", False)
        right = kwargs.get("right", False)
        
        if left:
            character.direction = "left"
            self.accelerate(0, character)
            character.acc.x -= character.vel.x * character.friction
            character.vel.x -= character.acc.x
            character.pos.x -= character.vel.x + 0.5 * character.acc.x
            character.rect.x = character.pos.x
            
        if right:
            character.direction = "right"
            self.accelerate(0, character)
            character.acc.x += character.vel.x * character.friction
            character.vel.x += character.acc.x
            character.pos.x += character.vel.x + 0.5 * character.acc.x
            character.rect.x = character.pos.x


class VerticalMovement(Movement):
    def execute(self, character: 'Character'):
        self.accelerate(1, character)
        character.acc.y += character.vel.y * character.friction
        character.vel.y += character.acc.y
        character.pos.y += character.vel.y + 0.5 * character.acc.y
        character.rect.bottom = character.pos.y