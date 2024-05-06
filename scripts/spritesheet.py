import pygame
import flyweight

class Spritesheet:
    def __init__(self, characterName, spritesheetName):
        self.spritesheets = flyweight.get_image_dict("character", characterName, spritesheetName)

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x,y, width, height))
        return sprite
    
    def flip(self, sprites):
        return (pygame.transform.flip(sprite, True, False) for sprite in sprites)