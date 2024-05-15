import pygame
from scripts.settings import *
from scripts.gameobject import GameObject
from scripts.spritesheet import Spritesheet
from scripts.animation import Animation
from scripts.command import MoveLeft, MoveRight

class Player(GameObject):
    def __init__(
        self,
        spritesheet,
        x,
        y,
        vel_x,
        vel_y,
        acl_x,
        acl_y,
        max_vel_x,
        max_vel_y
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
        self.image = self.sprites[0]
        self.animation = Animation(self.sprites)
        # self.mask = None
        self.rect = spritesheet.rect
        # self.direction = "left"

    def move(self, keys):
        
        if keys[pygame.K_LEFT]:
            MoveLeft.execute(self)
        if keys[pygame.K_RIGHT]:
            MoveRight.execute(self)

    def get_sprites(self, spritesheet):
        finn = Spritesheet(spritesheet.image)
        finn.get_sprites(200,200)
        finnScaled = finn.scaleSprites(0.64)
        return finnScaled
    
    def update(self):
        # self.rect.topleft = (self.x, self.y)
        self.image = self.animation.update()
        keys = pygame.key.get_pressed()
        self.move(keys)
        
                # if event.type == pygame.KEYUP:
                #     pass