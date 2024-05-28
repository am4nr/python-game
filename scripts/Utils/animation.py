import pygame
from scripts.Utils.utils import trim_surface



class Animation:
    def __init__(self):
        self.img_dur = 10
        self.frame = 0
        self.currentAnimIdx = 0
        self.images = []

    def update(self):
        self.frame += 1
        if self.frame >= self.img_dur:
            self.frame = 0
            self.currentAnimIdx += 1
        if self.currentAnimIdx >= len(self.images) - 1:
            self.currentAnimIdx = 0
        # return trim_surface(self.images[self.currentAnimIdx])
        return self.images[self.currentAnimIdx]

    def get_images(self, sprites, direction):
        if direction == "left":
            self.flip(sprites)
        elif direction == "right":
            self.get_surfaces(sprites)

    def get_img_dur(self, img_dur):
        self.img_dur = img_dur

    def get_surfaces(self, sprites):
        self.images = []
        for sprite in sprites:
            self.images.append(sprite.image)

    def flip(self, sprites):
        self.images = []
        for sprite in sprites:
            self.images.append(pygame.transform.flip(sprite.image, True, False))

    def reset(self):
        self.frame = 0
        self.currentAnimIdx = 0