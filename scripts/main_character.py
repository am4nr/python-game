from scripts.settings import *

class Entity:
    def __init__(self, x, y, vel_x, vel_y, acl_x, acl_y, sprite, max_vel_x = MAX_VEL_X, max_vel_y = MAX_VEL_Y):
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
        # Image
        self.image = sprite.image
        self.image_rect = sprite.image_rect

    