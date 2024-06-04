import pygame
from scripts.Utils.collision import Collision


class GameObject(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
    #     self.collision = Collision(self.game)

    # def update(self):
    #     self.detect_collision()

    # def detect_collision(self): 
    #     collided = self.collision.object_collision(self.game.character, self)
        # print(collided)