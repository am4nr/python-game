from scripts.GameObjects.gameobject import GameObject
from scripts.Utils.animation import Animation
import random
import pygame


class Collectable(GameObject):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.y = y

        self.sprites = game.sprites.handle_spritesheetDictTransformation(
            game.sprites.get_spritesheets("collectables", "fruits"),
            32,
            32,
        )
        self.animation = Animation()
        self.animation.get_img_dur = 1
        self.animation.get_surfaces(self.sprites[self.get_random_image()])
        self.image = self.sprites[self.get_random_image()][0].image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        self.image = self.animation.update()
        # self.detect_collision()

    def get_random_image(self):
        randomChoice = random.choice(list(self.sprites.keys()))
        return randomChoice