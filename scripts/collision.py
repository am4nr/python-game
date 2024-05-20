import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.character import Character


class Collision:
    def __init__(self, game):
        self.game = game
        self.level_layers = game.levels[game.current_level].get_layers()["solid"]
        # print(self.level_layers["group"])
        self.solid_layer = self.level_layers["group"]
        # for sprite in self.solid_layer:
        # print(sprite.image)
        # print(self.solid_layer)

    def handle_vertical_collision(self, character: "Character"):
        collided_sprite = pygame.sprite.spritecollideany(character, self.solid_layer)

        if collided_sprite:
            print(collided_sprite.rect)
            if pygame.sprite.collide_mask(character, collided_sprite):
                if character.vel.y > 0:
                    character.rect.bottom = collided_sprite.rect.top
                    character.pos.y = collided_sprite.rect.top
                    # character.vel.y = 0
                    character.acc.y = 0
                    # character.jumps = 2
                elif character.vel.y < 0:
                    character.rect.top = collided_sprite.rect.bottom
                    character.vel.y = 1
                return True
        return False

    def handle_horizontal_collision(self, character: "Character", objects):
        pass

    def handle_object_collision(self, character: "Character", callback):
        pass
