class GameObject:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.image = sprite.image
        self.image_rect = sprite.image_rect
