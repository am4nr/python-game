import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.hit = False

    def render(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), [self.rect.x, self.rect.y+self.rect.height/4+2, self.rect.width, self.rect.height/4])
        pygame.draw.rect(screen, (150, 150, 150), [self.rect.x, self.rect.y+self.rect.height/4+2, self.val_to_pixel(), self.rect.height/4])
        handle_pos = self.val_to_pixel() + self.rect.x
        pygame.draw.circle(screen, "#b68f40", (handle_pos, self.rect.centery), int(self.rect.height / 2))

    def val_to_pixel(self):
        return int((self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width)

    def pixel_to_val(self, pixel):
        return self.min_val + (pixel / self.rect.width) * (self.max_val - self.min_val)

    def move_handle(self, pos):
        self.val = self.pixel_to_val(pos - self.rect.x)
        if self.val < self.min_val:
            self.val = self.min_val
        if self.val > self.max_val:
            self.val = self.max_val

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.hit = True
        else:
            self.hit = False

    def update(self, pos):
        if self.hit:
            self.move_handle(pos[0])
        