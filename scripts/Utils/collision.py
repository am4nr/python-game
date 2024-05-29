import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.Character.character import Character


class Collision:
    def __init__(self, game):
        self.game = game
        self.solid_layer = game.levels[game.current_level].get_layers()["solid"][
            "group"
        ]

    def handle_vertical_collision(self, character: "Character"):
        character.on_ground = False

        character.rect.update(character.pos, character.image.get_size())

        collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)
        
        if collided_sprite and pygame.sprite.collide_mask(character, collided_sprite):
            if character.vel.y > 0:
                character.rect.y = collided_sprite.rect.y - character.image.get_height()
                character.pos.y = character.rect.y
                character.vel.y = 0
                character.acc.y = 0
                character.jumps = 2
                print("collision1")
                character.on_ground = True
                
            elif character.vel.y < 0:
                character.rect.y = collided_sprite.rect.y + character.image.get_height()
                character.pos.y = character.rect.y
                character.vel.y = 0
                character.on_ground = False
                print("collision2")
            else:
                character.on_ground = False
            
    def handle_horizontal_collision(self, character: "Character"):
        character.collided_x = False
        character.rect.update(character.pos, character.image.get_size())

        character.rect.x += character.vel.x

        collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)
        if collided_sprite:
            if character.vel.x > 0:
                character.rect.x = collided_sprite.rect.left + character.image.get_width()
                character.pos.x = character.rect.x
                character.vel.x = 0
                character.acc.x = 0
                character.collided_x = True
            elif character.vel.x < 0:
                character.rect.x = collided_sprite.rect.right - character.image.get_width()
                character.pos.x = character.rect.x
                character.vel.x = 0
                character.acc.x = 0
            else:
                character.collided_x = False

        character.rect.x -= character.vel.x
 

    def handle_object_collision(self, character: "Character", callback):
        pass
