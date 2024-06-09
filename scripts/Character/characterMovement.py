from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.Character.character import Character


class Movement:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def execute(self, character: "Character"):
        raise NotImplementedError


class HorizontalMovement(Movement):
    def execute(self, character: "Character"):
        character.acc.x = 0

        if character.collided_x:
            character.acc.x = 0
        elif character.direction == "left":
            character.acc.x = -character.speed
        elif character.direction == "right":
            character.acc.x = character.speed

        if character.acc.x != 0:
            character.acc.x *= 0.7071

        character.acc.x += character.vel.x * character.friction
        character.vel.x += character.acc.x
        character.pos.x += character.vel.x + 0.5 * character.acc.x
        character.rect.x = character.pos.x


class VerticalMovement(Movement):
    def execute(self, character: "Character"):
        character.acc.y = 0

        if character.jumping:
            character.acc.y = -character.speed
        elif character.on_ground or character.collided_y:
            character.acc.y = 0
        elif not character.jumping and not character.on_ground:
            character.acc.y = character.speed

        if character.acc.y != 0:
            character.acc.y *= 0.7071

        character.acc.y += character.vel.y * character.friction
        character.vel.y += character.acc.y
        character.pos.y += character.vel.y + 0.5 * character.acc.y
        character.rect.y = character.pos.y

