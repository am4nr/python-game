import pygame
from scripts.settings import *
from scripts.gameobject import GameObject
from scripts.spritesheet import Spritesheet
from scripts.animation import Animation

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
        self.sprites = self.get_sprites(spritesheet)
        self.image = self.sprites[4]
        self.animation = Animation(self.sprites)
        # self.mask = None
        self.rect = spritesheet.image_rect
        # self.direction = "left"

    def move(self, dir_x, dir_y):
        self.rect.x += dir_x
        self.rect.y += dir_y

    def get_sprites(self, spritesheet):
        finn = Spritesheet(spritesheet.image)
        finn.get_sprites(200,200)
        finnScaled = finn.scaleSprites(0.64)
        return finnScaled
    
    def update(self):
        self.image = self.animation.update()