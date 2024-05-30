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
        
    # def handle_collision(self, character:"Character"):
    #     vertical_collision_list= self.detect_vertical_collision(character)
    #     horizontal_collision_list = self.detect_horizontal_collision(character)
       
                            
    #     if vertical_collided_sprite is not None and horizontal_collided_sprite is not None:
    #         v_vec = pygame.Vector2(vertical_collided_sprite.rect.topleft)
    #         h_vec = pygame.Vector2(horizontal_collided_sprite.rect.topleft)
    #         if vertical_collided_sprite == horizontal_collided_sprite:
    #             if abs(character.rect.x - h_vec[0]) < character.rect.width - (character.vel.x):
    #                 self.resolve_vertical_collision(character, vertical_collided_sprite)
    #             else:
    #                self.resolve_horizontal_collision(character, horizontal_collided_sprite)
              
    #         # if vertical_collided_sprite is not None:
    #         #     self.resolve_vertical_collision(character, vertical_collided_sprite)
                
    #         # else:
    #         #     self.resolve_horizontal_collision(character, horizontal_collided_sprite)
    #         #     self.resolve_vertical_collision(character, vertical_collided_sprite)
                
    #     else:
    #         if vertical_collided_sprite is not None:
    #             self.resolve_vertical_collision(character, vertical_collided_sprite)
                
    #         if horizontal_collided_sprite is not None:
    #             self.resolve_horizontal_collision(character, horizontal_collided_sprite)
                
    # def handle_vertical_collision(self, character: "Character"):
    #     character.on_ground = False
    #     collided_sprite = self.detect_vertical_collision(character)
    #     self.resolve_vertical_collision(character, collided_sprite)


    def detect_vertical_collision(self, character: "Character"):
        character.on_ground = False
        # character.rect.update(character.pos, character.image.get_size())
        collision_list = pygame.sprite.spritecollide(character, self.solid_layer, False)
        
        return collision_list

    def resolve_vertical_collision(self, character: "Character"):
        collision_list = self.detect_vertical_collision(character)
        for collided_sprite in collision_list:
            #move down
            if character.vel.y >= 0: 
                character.rect.y = collided_sprite.rect.top -1
                character.pos.y = character.rect.y
                character.vel.y = 0
                character.jumps = 2
                # print("collision1")
                character.on_ground = True

            #move up    
            elif character.vel.y < 0: 
                character.rect.y = collided_sprite.rect.bottom + 1
                character.pos.y = character.rect.y
                character.vel.y = 0
                character.on_ground = False
                # print("collision2")
            else:
                character.on_ground = False

    # def handle_horizontal_collision(self, character:"Character"):
    #     character.collided_x = False
    #     collided_sprite = self.detect_vertical_collision(character)
    #     self.resolve_vertical_collision(character, collided_sprite)

    def detect_horizontal_collision(self, character: "Character"):
        character.collided_x = False
        # collided_sprite = self.detect_vertical_collision(character)
        # character.rect.update(character.pos, character.image.get_size())
        # character.rect.x += character.vel.x

        collision_list= pygame.sprite.spritecollide(character, self.solid_layer, False)
        return collision_list

    def resolve_horizontal_collision(self, character: "Character"):
        collision_list = self.detect_horizontal_collision(character)
        if collision_list:
            for collided_sprite in collision_list:
            #move right
                if character.vel.x > 0: 
                    character.rect.x = collided_sprite.rect.left - character.rect.width
                    # character.rect.right = collided_sprite.rect.left
                    # character.pos.x = character.rect.x
                    # character.vel.x = -1
                    # print("collision2")
                    character.collided_x = True
            #move left    
                elif character.vel.x < 0: 
                    character.rect.x = collided_sprite.rect.left
                    # character.vel.x = +1
                    # print("collision3")
                    # character.pos.x = character.rect.x
                    
                    character.collided_x = True
                else:
                    # character.rect.x -= character.vel.x
                    character.collided_x = False

        
    def handle_object_collision(self, character: "Character", callback):
        pass
