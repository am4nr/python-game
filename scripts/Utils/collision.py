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
        
        if collided_sprite:
            if pygame.sprite.collide_rect(character, collided_sprite):
                
                if character.vel.y > 0:
                    character.rect.bottom = collided_sprite.rect.top
                    character.pos.y = character.rect.y
                    character.vel.y = 0
                    character.acc.y = 0
                    character.jumps = 2
                    print("collision1")
                    character.on_ground = True
                    
                    
                elif character.vel.y < 0:
                    character.rect.top = collided_sprite.rect.bottom
                    character.pos.y = character.rect.y
                    character.vel.y = 1
                    character.on_ground = False
                    print("collision2")
        else:
            character.on_ground = False
            
    def handle_horizontal_collision(self, character: "Character"):
        character.collided_x = False
        character.rect.update(character.pos, character.image.get_size())

        # next_rect = character.rect.copy()
        # if character.direction == "left":
        #     next_rect.x = character.rect.x + character.vel.x
        # elif character.direction == "right":
        #     next_rect.x = character.rect.x + character.vel.x

        character.rect.x += character.vel.x


        collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)
        # print(next_rect, "vs", character.rect)

        if collided_sprite:
            # if next_rect.colliderect(collided_sprite):
            if pygame.sprite.collide_rect(character, collided_sprite):
                # character.vel.x = 0
                if character.vel.x > 0:
                    character.rect.right = collided_sprite.rect.left - 5
                    character.pos.x = character.rect.x
                    character.vel.x = 0
                    character.collided_x = True
                elif character.vel.x < 0:
                    character.rect.left = collided_sprite.rect.right + 10
                    character.pos.x = character.rect.x
                    character.vel.x = 0
                    character.collided_x = True

                # if character.rect.right >= collided_sprite.rect.left and character.direction == "right":
            #     character.collided_x = True
            #     print("collision3")
            # elif character.rec.left <= collided_sprite.rect.right and character.direction == "left":
            #          character.collided_x = True
            #          print("collision4")
                
                # character.vel.x = 0
                # character.acc.x = 0
                print("collision5")
            else:
                character.collided_x = False

        character.rect.x -= character.vel.x
        # if character.direction == "left":
        #     character.rect.x += character.vel.x
        # elif character.direction == "right":
        #     character.rect.x -= character.vel.x


    def handle_object_collision(self, character: "Character", callback):
        pass
