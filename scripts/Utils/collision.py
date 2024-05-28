import pygame
from scripts.Character.characterMovement import HorizontalMovement
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.Character.character import Character


class Collision:
    def __init__(self, game):
        self.game = game
        self.solid_layer = game.levels[game.current_level].get_layers()["solid"][
            "group"
        ]
        self.collided = False

    def handle_vertical_collision(self, character: "Character"):
        #character.on_ground = False
        collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)
        
        if collided_sprite:
            if pygame.sprite.collide_rect(character, collided_sprite):
                
                if character.vel.y >= 0:
                    # character.rect.bottom = collided_sprite.rect.top
                    character.rect.bottom = collided_sprite.rect.top+5
                    # character.rect.bottom = character.pos.y
                    character.vel.y = 0
                    character.acc.y = 0
                    character.jumps = 2
                    print("collision1")
                    character.on_ground = True
                    
                    
                    
                elif character.vel.y < 0:
                    character.rect.top = collided_sprite.rect.bottom
                    character.vel.y = 1
                    character.on_ground = False
                    print("collision2")
        else:
            character.on_ground = False
            
    def handle_horizontal_collision(self, character: "Character"):
        
        # character.pos.x += character.vel.x * 2
        # character.update()
        HorizontalMovement().execute(character)
        collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)

        if collided_sprite:
            if pygame.sprite.collide_mask(character, collided_sprite):
                self.collided = True
                print("collision3")
            else:
                self.collided = False
        character.pos.x -= character.vel.x * 2
        # character.update()
        return self.collided
    

    def handle_object_collision(self, character: "Character", callback):
        pass
