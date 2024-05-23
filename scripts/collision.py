import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.character import Character


class Collision:
    def __init__(self, game):
        self.game = game
        self.solid_layer = game.levels[game.current_level].get_layers()["solid"][
            "group"
        ]


    def handle_vertical_collision(self, character: "Character"):
        collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)

        if collided_sprite:
            if pygame.sprite.collide_mask(character, collided_sprite):
                if character.vel.y > 0:
                    # character.rect.bottom = collided_sprite.rect.top
                    character.pos.y = collided_sprite.rect.top
                    character.vel.y = 0
                    character.acc.y = 0
                    character.jumps = 2
                elif character.vel.y < 0:
                    character.rect.top = collided_sprite.rect.bottom
                    character.vel.y = 1
                return True
        return False

    def handle_horizontal_collision(self, character: "Character", objects):
        pass

    def handle_object_collision(self, character: "Character", callback):
        pass
