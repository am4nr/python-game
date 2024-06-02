import pygame

vec = pygame.math.Vector2
class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, game, tilemap, platform_tiles, tile_width, tile_height, speed, path, direction):
        super().__init__()
        self.game = game
        self.tilemap = tilemap
        self.platform_tiles = platform_tiles
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.speed = speed
        self.path = path
        self.current_path_index = 0
        self.current_path = self.path[self.current_path_index]
        self.path_index = 0
        self.direction = direction
        self.image,self.rect = self.create_image_and_rect()
        
    def create_image_and_rect(self):
        # Determine the bounds of the platform
        min_col = min(tile % self.tilemap.width for tile in self.platform_tiles)
        max_col = max(tile % self.tilemap.width for tile in self.platform_tiles)
        min_row = min(tile // self.tilemap.width for tile in self.platform_tiles)
        max_row = max(tile // self.tilemap.width for tile in self.platform_tiles)

        platform_width = (max_col - min_col + 1) * self.tile_width
        platform_height = (max_row - min_row + 1) * self.tile_height

        platform_surf = pygame.Surface((platform_width, platform_height), pygame.SRCALPHA).convert_alpha()
        platform_surf.fill((0, 0, 0, 0))  # Ensure the surface is transparent

        for tile_index in self.platform_tiles:
            col = tile_index % self.tilemap.width
            row = tile_index // self.tilemap.width
            solid_tile_id = self.tilemap.layers["solid"]["data"][tile_index]
            solid_tile_surf = self.tilemap.get_tile_surface(solid_tile_id)
            self.tilemap.layers["solid"]["data"][tile_index] = 0

            platform_surf.blit(solid_tile_surf, ((col - min_col) * self.tile_width, (row - min_row) * self.tile_height))
            rect = pygame.rect.Rect(
            min_col * self.tile_width,
            min_row * self.tile_height,
            platform_width,
            platform_height,
        )
        return platform_surf, rect
    
    
    def update(self):
        if self.path:
            target_pos = self.path[self.path_index]
            moving_direction_x = None
            moving_direction_y = None
            
            # Calculate the direction vector
            if self.direction == "vertical":
                if target_pos[1] > self.rect.y: # move down
                    direction_vector = vec(0, self.speed)
                    moving_direction_y = "down"
                else: # move up
                    direction_vector = vec(0, -self.speed)
                    moving_direction_y = "up"
                    
            elif self.direction == "horizontal":
                if target_pos[0] > self.rect.x: # move right
                    direction_vector = vec(self.speed,0)
                    moving_direction_y = "right"
                else: # move left
                    direction_vector = vec(-self.speed, 0)
                    moving_direction_y = "left"
                    
                    
                #direction_vector = vec(self.speed if target_pos[0] > self.rect.x else -self.speed, 0)

            # Move the platform
            self.rect.move_ip(direction_vector)

            # Check if the platform has reached the target position
            """ if self.direction == "vertical":
                if self.rect.y == target_pos[1]:
                    self.path_index = (self.path_index + 1) % len(self.path)
                    if self.path_index == 0 or self.path_index == len(self.path):
                        self.path = list(reversed(self.path)) """
                        
            if (self.direction == "horizontal" and self.rect.x == target_pos[0]) or (self.direction == "vertical" and self.rect.y == target_pos[1]):
                self.path_index = (self.path_index + 1) % len(self.path)
                if self.path_index == 0 or self.path_index == len(self.path):
                    self.path = list(reversed(self.path))
            
            """ if self.rect.y == target_pos[1] or self.rect.left == target_pos[0] or self.rect.right == target_pos[0]:
                self.path_index = (self.path_index + 1) % len(self.path)
                if self.path_index == 0 or self.path_index == len(self.path):
                    self.path = list(reversed(self.path)) """

        
    def draw(self, screen):
        screen.blit(self.image, self.rect)