import pygame
from scripts.Utils.utils import trim_surface



class Animation:
    def __init__(self):
        self.img_dur = 10
        self.frame = 0
        self.currentAnimIdx = 0
        self.images = []
        self.done = False
        self.loop = True

    def update(self):
        self.frame += 1
        if self.frame >= self.img_dur:
            self.frame = 0
            self.currentAnimIdx += 1
        if self.currentAnimIdx >= len(self.images) - 1:
            self.currentAnimIdx = 0
            if not self.loop:
                self.done = True

        return trim_surface(self.images[self.currentAnimIdx])
        #return self.images[self.currentAnimIdx]
    
    def check_done(self):
        return self.done

    def get_images(self, sprites, direction):
        if direction == "left":
            self.flip(sprites)
        elif direction == "right":
            self.get_surfaces(sprites)

    def get_surfaces(self, sprites):
        self.images = []
        for sprite in sprites:
            self.images.append(sprite.image)

    def flip(self, sprites):
        self.images = []
        for sprite in sprites:
            self.images.append(pygame.transform.flip(sprite.image, True, False))

    def reset(self, sprites, direction, loop = True, img_dur = 12, next_state = None):
        self.frame = 0
        self.currentAnimIdx = 0
        self.img_dur = img_dur
        self.loop = loop
        self.get_images(sprites, direction)
        self.done = False