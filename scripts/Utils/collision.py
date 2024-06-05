import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.Character.character import Character


class Collision:
    def __init__(self, game):
        self.game = game
        self.solid_layer = self.game.level_manager.current_level.solid_layer
        self.gameObjects = self.game.level_manager.current_level.gameObjects


    def detect_horizontal_collision(self, character: "Character"):
        character.collided_x = False

        character.rect.update(
            (character.rect.x, character.rect.bottom - character.image.get_height()),
            character.image.get_size(),
        )
        if character.direction == "left":
            character.rect.left -= 3
        elif character.direction == "right":
            character.rect.right += 3

        collision_list = pygame.sprite.spritecollide(character, self.solid_layer, False)
        if character.direction == "left":
            character.rect.left += 3
        elif character.direction == "right":
            character.rect.right -= 3
        return collision_list

    def horizontal_collision(self, character: "Character"):
        # for tile in self.solid_layer.sprites():
        #     if tile.rect.colliderect(character.rect.x + character.dx, character.rect.y, character.rect.width, character.rect.height):
        collision_list = self.detect_horizontal_collision(character)
        if collision_list:
            for collided_sprite in collision_list:
                if character.vel.x > 0:
                    character.pos.x = (
                        collided_sprite.rect.left - character.rect.width - 3
                    )
                    character.rect.x = character.pos.x
                    character.vel.x = 0
                    character.collided_x = True
                    return

                # moving left
                elif character.vel.x < 0:
                    character.pos.x = collided_sprite.rect.right + 3
                    character.rect.x = character.pos.x
                    character.vel.x = 0
                    character.collided_x = True
                    return

    def detect_vertical_collision(self, character: "Character"):
        character.on_ground = False
        character.collided_y = False

        character.rect.update(
            (character.rect.x, character.rect.bottom - character.image.get_height()),
            character.image.get_size(),
        )
        if character.jumping:
            character.rect.top -= 1
        else:
            character.rect.bottom += 3
        collision_list = pygame.sprite.spritecollide(character, self.solid_layer, False)
        if character.jumping:
            character.rect.top += 1
        else:
            character.rect.bottom -= 3

        return collision_list

    def vertical_collision(self, character: "Character"):
        # for tile in self.solid_layer.sprites():
        # if tile.rect.colliderect(character.rect.x, character.rect.y + character.dy, character.rect.width, character.rect.height):
        # check if below the ground i.e. jumping
        collision_list = self.detect_vertical_collision(character)
        if collision_list:
            for collided_sprite in collision_list:
                if character.vel.y >= 0:
                    character.on_ground = True
                    character.jumping = False
                    character.pos.y = collided_sprite.rect.top - character.rect.height
                    character.rect.y = character.pos.y
                    character.vel.y = 0
                    character.jumps = 2
                    return

                # moving up

                elif (
                    character.vel.y < 0
                    or character.vel.x < 0
                    and character.vel.y < 0
                    or character.vel.x > 0
                    and character.vel.y < 0
                ):
                    character.pos.y = collided_sprite.rect.bottom + 3
                    character.rect.y = character.pos.y
                    character.vel.y = 1
                    character.on_ground = False
                    character.jumping = False
                    character.jumps = 0
                    character.collided_y = True
                    return

    def object_collision(self, character):
        collision_list = pygame.sprite.spritecollide(character, self.gameObjects, False)

        for obj in collision_list: 
            if not obj.collided:
                obj.handle_collision()
                return