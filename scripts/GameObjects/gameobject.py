import pygame
from scripts.Utils.collision import Collision


class GameObject(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

    def update(self):
        pass
