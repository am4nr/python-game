import pygame
from scripts.settings import *
from scripts.gameobject import GameObject
from scripts.spritesheet import Spritesheet


class Player(GameObject):
    def __init__(
        self,
        x,
        y,
        spritesheet,
        vel_x=0,
        vel_y=0,
        acl_x=0,
        acl_y=0,
        max_vel_x=MAX_VEL_X,
        max_vel_y=MAX_VEL_Y,
    ):
        # Position
        self.x = x
        self.y = y
        # Velocity
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.max_vel_x = max_vel_x
        self.max_vel_y = max_vel_y
        # Accelaration
        self.acl_x = acl_x
        self.acl_y = acl_y
        #
        self.sprites = self.getSprite(spritesheet)
        self.scaledSprites = self.scaleSprites(self.sprites)
        self.image = self.scaledSprites[0]
        # self.mask = None
        self.rect = spritesheet.image_rect
        # self.direction = "left"

    def move(self, dir_x, dir_y):
        self.rect.x += dir_x
        self.rect.y += dir_y

    def getSprite(self,spritesheet):
        finn = Spritesheet(spritesheet.image)
        finn.get_sprites(200,200)
        return finn.sprites
    
    def scaleSprites(self, sprites):
        scaledSprites = []
        for sprite in sprites:
            scaledSprites.append(pygame.transform.scale_by(sprite, 0.32))
        return scaledSprites

    # def update(self):
