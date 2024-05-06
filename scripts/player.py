from utilities.settings import *
import pygame

class Entity:
    def __init__(self, x, y, width, height, vel_x=0, vel_y=0, acl_x=0, acl_y=0, image=None, max_vel_x = MAX_VEL_X, max_vel_y = MAX_VEL_Y):
        # Position
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Velocity
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.max_vel_x = max_vel_x
        self.max_vel_y = max_vel_y
        # Accelaration
        self.acl_x = acl_x
        self.acl_y = acl_y
        # 
        self.image = pygame.transform.scale(image, (width, height))
        #self.mask = None
        self.rect = pygame.Rect(x, y, width, height)
        #self.direction = "left"
    
    def move(self, dir_x, dir_y):
        self.rect.x += dir_x
        self.rect.y += dir_y
