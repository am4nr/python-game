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
        self.collided = False

    def handle_vertical_collision(self, character: "Character"):
        collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)

        if collided_sprite:
            if pygame.sprite.collide_mask(character, collided_sprite):
                if character.vel.y > 0:
                    # character.rect.bottom = collided_sprite.rect.top
                    character.pos.y = collided_sprite.rect.top
                    # character.rect.bottom = character.pos.y
                    character.vel.y = 0
                    character.acc.y = 0
                    character.jumps = 2
                    self.character.animation.get_images(
                        self.character.sprites["run"], True
                    )
                elif character.vel.y < 0:
                    character.rect.top = collided_sprite.rect.bottom
                    character.vel.y = 1
                return True
        return False

    def handle_horizontal_collision(self, character: "Character", objects):
        
        character.pos.x += self.vel.x * 2
        character.update()
        collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)

        if collided_sprite:
            if pygame.sprite.collide_mask(character, collided_sprite):
                self.collided = True
            else:
                self.collided = False
        character.pos.x -= self.vel.x * 2
        character.update()
        return self.collided
    

    def handle_object_collision(self, character: "Character", callback):
        pass