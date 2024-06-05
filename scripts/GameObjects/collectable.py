from scripts.GameObjects.gameobject import GameObject
from scripts.Utils.animation import Animation
import random
import pygame
vec = pygame.math.Vector2

class Collectable(GameObject):
    def __init__(self, game, x, y):
        self.game = game
        super().__init__(game)
        self.x = x
        self.y = y

        self.sprites = game.sprites.handle_spritesheetDictTransformation(
            game.sprites.get_spritesheets("collectables", "fruits"),
            32,
            32,
        )
        self.collectedanimation = game.sprites.handle_spritesheetDictTransformation(
            game.sprites.get_spritesheets("collectables", "effects"),
            32,
            32,
        )
        self.animation = Animation()
        self.animation.get_img_dur = 6
        self.animation.get_surfaces(self.sprites[self.get_random_image()])
        self.image = self.sprites[self.get_random_image()][0].image
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.collided = False


    def update(self):
        self.image = self.animation.update()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.remove()

    def get_random_image(self):
        randomChoice = random.choice(list(self.sprites.keys()))
        return randomChoice
    
    def handle_collision(self):
        self.animation.reset(self.collectedanimation["Collected"], "right", False, 3)

    def remove(self):
        if self.animation.check_done():
            self.game.level_manager.current_level.gameObjects.remove(self)