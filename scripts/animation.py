import pygame

class Animation:
    def __init__(self, sprites, img_dur = 12):
        self.sprites = sprites
        self.img_dur = 12
        self.frame = 0
        self.currentAnimIdx = 0

    def update(self):
        self.frame += 1
        if self.frame >= self.img_dur:
            self.frame = 0
            self.currentAnimIdx += 1
        if self.currentAnimIdx >= len(self.images) - 1:
                self.currentAnimIdx = 0
        return self.sprites[self.currentAnimIdx]

    # def get_image(self, images):
    #     self.images = images
    
    # def get_img_dur(self, img_dur):
    #     self.img_dur = img_dur

    def flip(self):
        flippedSprites = []
        for sprite in self.sprites:
            flippedSprites.append(pygame.transform.flip(sprite, True, False))
        return flippedSprites

    def reset(self, images, img_dur = 12):
        self.frame = 0
        self.currentAnimIdx = 0
        self.img_dur = img_dur
        self.images = images