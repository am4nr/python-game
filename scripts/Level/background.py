import pygame

class Background:
    def __init__(self, game, background_images, parallax_images):
        self.game = game
        self.background_images = []
        for image in background_images:
            self.background_images.append(self.game.assets.get(image))
        self.parallax_images = []
        for image in self.parallax_images:
            self.parallax_images.append(self.game.assets.get(image))
    