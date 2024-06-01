import pygame
class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, game, tilemap, platform_tiles, tile_width, tile_height, speed):
        super().__init__()
        self.game = game
        self.tilemap = tilemap
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.speed = speed
        self.create_platform(platform_tiles)

    def create_platform(self, platform_tiles):
        min_col = min(tile_index % self.tilemap.width for tile_index in platform_tiles)
        max_col = max(tile_index % self.tilemap.width for tile_index in platform_tiles)
        min_row = min(tile_index // self.tilemap.width for tile_index in platform_tiles)
        max_row = max(tile_index // self.tilemap.width for tile_index in platform_tiles)

        platform_width = (max_col - min_col + 1) * self.tile_width
        platform_height = (max_row - min_row + 1) * self.tile_height

        platform_surf = pygame.Surface((platform_width, platform_height), pygame.SRCALPHA).convert_alpha()

        for tile_index in platform_tiles:
            col = tile_index % self.tilemap.width
            row = tile_index // self.tilemap.width
            solid_tile_id = self.tilemap.layers["solid"]["data"][tile_index]
            solid_tile_surf = self.tilemap.get_tile_surface(solid_tile_id)
            self.tilemap.layers["solid"]["data"][tile_index] = 0

            platform_surf.blit(solid_tile_surf, ((col - min_col) * self.tile_width, (row - min_row) * self.tile_height))

        self.sprite = self.game.assets.get("Sprite", platform_surf)
        self.sprite.rect = pygame.rect.Rect(
            min_col * self.tile_width,
            min_row * self.tile_height,
            platform_width,
            platform_height,
        )

        self.rect = self.sprite.rect.copy()
        self.path = [self.rect.copy()]

    def update(self):
        # Move the platform along its path
        """ next_rect = self.path[self.index]
        if self.direction == 0:  # Horizontal movement
            if self.rect.x < next_rect.x:
                self.rect.x += self.speed
            elif self.rect.x > next_rect.x:
                self.rect.x -= self.speed
            else:
                self.index = (self.index + 1) % len(self.path)
        else:  # Vertical movement
            if self.rect.y < next_rect.y:
                self.rect.y += self.speed
            elif self.rect.y > next_rect.y:
                self.rect.y -= self.speed
            else:
                self.index = (self.index + 1) % len(self.path) """

        self.sprite.rect = self.rect  # Update the sprite's rect
        
    def draw(self, screen):
        screen.blit(self.sprite.image, self.sprite.rect)