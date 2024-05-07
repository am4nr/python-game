import pygame

class Spritesheet:
    def __init__(self, spritesheet):
        self.spritesheet = spritesheet
        self.sprites = []

    def get_sprites(self, width, height):
        for i in range(self.spritesheet.get_width() // width):
            surface = pygame.Surface((width,height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(self.spritesheet, (0,0), rect)
            self.sprites.append(surface)

    
    def flip(self, sprites):
        return (pygame.transform.flip(sprite, True, False) for sprite in sprites)