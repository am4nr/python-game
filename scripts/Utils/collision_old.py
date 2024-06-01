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

        # character.rect.update((character.rect.x, character.rect.bottom - character.image.get_height()), character.image.get_size())
        if character.jumping:
            character.rect.top -= 1
        else:
            character.rect.bottom += 1
        collision_list = pygame.sprite.spritecollide(character, self.solid_layer, False)

        return collision_list

    def resolve_vertical_collision(self, character: "Character"):
        collision_list = self.detect_vertical_collision(character)
        for collided_sprite in collision_list:
            print("Vertical Collision")
            self.get_direction(character, collided_sprite)
            # moving down
            if character.vel.y >= 0:
                character.on_ground = True
                character.jumping = False
                character.pos.y = collided_sprite.rect.top - character.rect.height
                character.rect.y = character.pos.y
                character.vel.y = 0
                character.jumps = 2
                return

            # moving up
            elif character.vel.y < 0:
                print("collision!")
                character.pos.y = collided_sprite.rect.bottom
                character.rect.y = character.pos.y
                character.vel.y = 1
                character.on_ground = False
                character.jumping = False
                return
            else:
                character.on_ground = False
                return

    # def handle_horizontal_collision(self, character:"Character"):
    #     collided_sprite = self.detect_vertical_collision(character)
    #     self.resolve_vertical_collision(character, collided_sprite)

    def detect_horizontal_collision(self, character: "Character"):
        character.collided_x = False
        character.on_ground = False
        # collided_sprite = self.detect_vertical_collision(character)
        # character.rect.update(
        #     (character.rect.x, character.rect.bottom - character.image.get_height()),
        #     character.image.get_size(),
        # )

        character.rect.x += character.vel.x
        character.rect.y += character.vel.y
        # next_move.move_ip(character.vel.x, character.vel.y)
        # collision_list = pygame.sprite.spritecollide(character, self.solid_layer, False)
        collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)
        # collision_list = next_move.collidelist
        if collided_sprite:
            #print("collided horizontal")
            direction = self.get_direction(character, collided_sprite)
            #print(direction)
        character.rect.x -= character.vel.x
        character.rect.y -= character.vel.y

        if collided_sprite:
            return direction, collided_sprite
        else:
            return None, None

    def resolve_horizontal_collision(self, character: "Character"):
        direction, collided_sprite = self.detect_horizontal_collision(character)
        # if collision_list:
        # for collided_sprite, direction in collision_list, direction_list:
        # print("Horizontal Collision")
        # self.get_direction(character, collided_sprite)
        # moving right
        if direction and collided_sprite:
            if "left" == direction:
                character.rect.left = collided_sprite.rect.right
                character.pos.x = collided_sprite.rect.left
                character.vel.x = 0
                print("left")

            if "right" == direction:
                character.rect.right = collided_sprite.rect.left
                character.pos.x = collided_sprite.rect.right
                character.vel.x = 0
                print("right")

            if "top" == direction:
                character.rect.top = collided_sprite.rect.bottom
                character.pos.y = collided_sprite.rect.bottom
                character.on_ground = False
                character.vel.y = 0
                print("top")

            if "bottom" == direction:
                character.rect.bottom = collided_sprite.rect.top
                character.pos.y = collided_sprite.rect.top - character.rect.height
                character.vel.y = 0
                character.jumps = 2
                character.on_ground = True
                print("bottom")

        """ if character.vel.x > 0: 
            character.pos.x = collided_sprite.rect.left - character.rect.width
            character.rect.x = character.pos.x
            character.vel.x = 0
            return

        #moving left    
        elif character.vel.x < 0: 
            character.pos.x = collided_sprite.rect.right
            character.rect.x = character.pos.x
            character.vel.x = 0
            return """

    """ def get_direction(self, character, collided_sprite):
        # character.rect.update(
        #     (character.rect.x, character.rect.bottom - character.image.get_height()),
        #     character.image.get_size(),
        # )

        # collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)

        collided_vec = {}
        collided_vec.update({"top": pygame.Vector2(collided_sprite.rect.midtop)})
        collided_vec.update({"left": pygame.Vector2(collided_sprite.rect.midleft)})
        collided_vec.update({"right": pygame.Vector2(collided_sprite.rect.midright)})
        collided_vec.update({"bottom": pygame.Vector2(collided_sprite.rect.midbottom)})
        # print(collided_vec)
        # character_pos = pygame.Vector2(character.rect.center)
        character_vec = {}
        character_vec.update({"left": pygame.Vector2(character.rect.midleft)})
        character_vec.update({"right": pygame.Vector2(character.rect.midright)})
        character_vec.update({"top": pygame.Vector2(character.rect.midtop)})
        character_vec.update({"bottom": pygame.Vector2(character.rect.midbottom)})

        dif_vec = {}
        dif_vec.update(
            {"bottom": character_vec["bottom"].distance_to(collided_vec["top"])}
        )
        dif_vec.update(
            {"left": character_vec["left"].distance_to(collided_vec["right"])}
        )
        dif_vec.update(
            {"right": character_vec["right"].distance_to(collided_vec["left"])}
        )
        dif_vec.update(
            {"top": character_vec["top"].distance_to(collided_vec["bottom"])}
        )
        # print(dif_vec)
        sorted_dif = sorted(dif_vec.items(), key=lambda x: x[1])
        # print(sorted_dif[0])

        return sorted_dif[0] """
        
    def get_direction(self, character, collided_sprite):
        # Calculate the distances between relevant edges
        bottom_distance = abs(character.rect.top - collided_sprite.rect.bottom)
        top_distance = abs(character.rect.bottom - collided_sprite.rect.top)
        left_distance = abs(character.rect.right - collided_sprite.rect.left)
        right_distance = abs(character.rect.left - collided_sprite.rect.right)

        # Determine the collision direction based on distances and character's velocity
        if character.vel.y < 0 and bottom_distance < top_distance:
            return "top"
        elif character.vel.y > 0 and top_distance < bottom_distance:
            return "bottom"
        elif character.vel.x > 0 and left_distance < right_distance:
            return "left"
        elif character.vel.x < 0 and right_distance < left_distance:
            return "right"

    def handle_object_collision(self, character: "Character", callback):
        pass
