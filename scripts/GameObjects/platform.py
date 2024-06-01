import pygame
class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, game, tilemap, platform_tiles, tile_width, tile_height, speed, path, direction):
        super().__init__()
        self.game = game
        self.tilemap = tilemap
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.speed = speed
        self.path = path
        self.current_path_index = 0
        self.current_path = self.path[self.current_path_index]
        self.path_index = 0
        self.direction = direction
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
        #self.path = path

    def update(self):
        if self.path:
            current_pos = (self.rect.x // self.tile_width, self.rect.y // self.tile_height)
            target_index = self.current_path[self.path_index]
            target_pos = (target_index % self.tilemap.width, target_index // self.tilemap.width)

            if current_pos != target_pos:
                if self.direction == "vertical":
                    if current_pos[1] < target_pos[1]:
                        self.rect.y += self.speed
                    elif current_pos[1] > target_pos[1]:
                        self.rect.y -= self.speed
                elif self.direction == "horizontal":
                    if current_pos[0] < target_pos[0]:
                        self.rect.x += self.speed
                    elif current_pos[0] > target_pos[0]:
                        self.rect.x -= self.speed
            else:
                self.path_index += 1
                if self.path_index >= len(self.current_path):
                    self.current_path_index = (self.current_path_index + 1) % len(self.path)
                    self.current_path = self.path[self.current_path_index]
                    self.path_index = 0

            self.sprite.rect = self.rect



        
    def draw(self, screen):
        screen.blit(self.sprite.image, self.sprite.rect)