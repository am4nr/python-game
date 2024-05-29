import pygame

class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, sprite, path, speed):
        super().__init__()
        self.sprite = sprite  # Store the sprite reference
        self.image = sprite.image
        self.rect = sprite.rect.copy()
        self.path = path
        self.speed = speed
        self.direction = 0
        self.index = 0

    def update(self):
        # Move the platform along its path
        next_rect = self.path[self.index]
        if self.rect.x < next_rect.x:
            self.rect.x += self.speed
            self.sprite.rect.x = self.rect.x  # Update the sprite's rect
            self.direction = 0
        elif self.rect.x > next_rect.x:
            self.rect.x -= self.speed
            self.sprite.rect.x = self.rect.x  # Update the sprite's rect
            self.direction = 0
        elif self.rect.y < next_rect.y:
            self.rect.y += self.speed
            self.sprite.rect.y = self.rect.y  # Update the sprite's rect
            self.direction = 1
        elif self.rect.y > next_rect.y:
            self.rect.y -= self.speed
            self.sprite.rect.y = self.rect.y  # Update the sprite's rect
            self.direction = 1
        else:
            self.index = (self.index + 1) % len(self.path)
