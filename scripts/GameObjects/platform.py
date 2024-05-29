class MovingPlatform:
    def __init__(self, sprite, path, speed):
        self.sprite = sprite
        self.path = path
        self.speed = speed
        self.direction = 0  # Assume horizontal movement initially
        self.index = 0

    def update(self):
        # Move the platform along its path
        next_rect = self.path[self.index]
        if self.sprite.rect.x < next_rect.x:
            self.sprite.rect.x += self.speed
            self.direction = 0  # Horizontal movement
        elif self.sprite.rect.x > next_rect.x:
            self.sprite.rect.x -= self.speed
            self.direction = 0  # Horizontal movement
        elif self.sprite.rect.y < next_rect.y:
            self.sprite.rect.y += self.speed
            self.direction = 1  # Vertical movement
        elif self.sprite.rect.y > next_rect.y:
            self.sprite.rect.y -= self.speed
            self.direction = 1  # Vertical movement
        else:
            # Reached the next point in the path
            self.index = (self.index + 1) % len(self.path)