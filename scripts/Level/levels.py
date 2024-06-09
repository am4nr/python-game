import pygame
from scripts.Character.characters import Finn, Quack
from scripts.Utils.settings import WIDTH, HEIGHT
from scripts.Level.background import Background
from scripts.UI.healthbar import Healthbar

vec = pygame.math.Vector2
BG1 = Background("1")
BG2 = Background("2")
BG3 = Background("3")
BG4 = Background("4")

levels = [
    {"level_name": "Test-Level", "character": Quack, "background": BG1, "health": 3},
    {"level_name": "Test-Level2", "character": Finn, "background": BG2, "health": 3},
    {"level_name": "Level2", "character": Quack, "background": BG3, "health": 3},
    {"level_name": "Level1", "character": Quack, "background": BG4, "health": 3},
]


class LevelManager:
    def __init__(self, game):
        self.game = game
        self.levels = []
        self.current_level = None
        self.load_levels()

    def set_level(self, level_id):
        for level in self.levels:
            if level_id == level.id:
                self.current_level = level
                self.current_level.load()

    def next_level(self):
        index = 0
        for level in self.levels:
            if level.id == self.current_level.id:
                index = self.levels.index(level)

        if index == len(self.levels) - 1:
            self.current_level = self.levels[0]
        else:
            self.current_level = self.levels[index + 1]

        self.current_level.load()

    def load_levels(self):
        for level in levels:
            level_name = level.get("level_name")
            character = level.get("character")
            background = level.get("background")
            health = level.get("health")
            character.game = self.game
            if len(self.levels) == 0:
                self.current_level = Level(
                    self.game,
                    level_name,
                    len(self.levels),
                    character,
                    background,
                    health,
                )
                self.levels.append(self.current_level)
            else:
                self.levels.append(
                    Level(
                        self.game,
                        level_name,
                        len(self.levels),
                        character,
                        background,
                        health,
                    )
                )


class Level:
    def __init__(self, game, level_name, level_id, character, background, health):
        self.game = game
        self.tilemap = game.assets.get("Tilemap", level_name)
        self.tilesets = self.tilemap.tilesets
        self.tiles = {}
        self.collectables = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.gameObjects = pygame.sprite.Group()
        self.levelObjects = []
        self.id = level_id
        self.moving_platforms = []
        self.character = character
        self.offset_x = 0
        self.offset_y = self.tilemap.height * self.tilemap.tile_height - HEIGHT
        self.background = background
        self.healthbar = Healthbar(self.game, 50, 50)
        self.character_max_health = health

    def load(self):
        self.gameObjects = pygame.sprite.Group()
        self.tilemap.load_layers()
        self.moving_platforms = self.tilemap.layers["gameObjects"]["moving_platforms"]
        self.solid_layer = self.tilemap.layers["solid"]["group"]
        self.background.load(self.game)
        
        for platform in self.moving_platforms:
            self.solid_layer.add(
                platform
            )
            
        # Add the platform sprite to the gameObjects group
        self.gameObjectsLayer = self.tilemap.layers["gameObjects"]
        self.collectables = self.gameObjectsLayer["collectables"]
        self.traps = self.gameObjectsLayer["traps"]
        self.spawn = self.gameObjectsLayer["spawn"]
        self.goal = self.gameObjectsLayer["goal"]

        self.gameObjects.add(self.collectables)
        self.gameObjects.add(self.traps)
        
        self.character.pos = vec(self.spawn[0], self.spawn[1])
        self.character.load()
        self.character.health = self.character_max_health
        
        self.goal.load()

        self.healthbar.load()

        self.offset_x = 0
        self.offset_y = self.tilemap.height * self.tilemap.tile_height - HEIGHT

    def update(self):
        for platform in self.moving_platforms:
            platform.update()
        self.character.update()
        self.set_offset()
        self.healthbar.update()
        self.background.update()
        self.collectables.update()
        self.traps.update()
        self.goal.update()
        if self.character.health <= 0:
            self.game.changeState(self.game.states["GameOver"])
            
    def check_goal(self):
        if self.goal.state == "active":
            if self.character.rect.colliderect(self.goal.rect):
                self.game.level_manager.next_level()
            
    def set_offset(self):
        scroll_area_width = WIDTH * 0.2
        
        tilemap_width = self.tilemap.width * self.tilemap.tile_width
        tilemap_height = self.tilemap.height * self.tilemap.tile_height

        if tilemap_width <= WIDTH:
            return
        elif (
            (self.character.rect.right - self.offset_x >= WIDTH - scroll_area_width)
            and self.character.vel.x > 0
        ) or (
            (self.character.rect.left - self.offset_x <= scroll_area_width)
            and self.character.vel.x < 0
        ):
            self.offset_x += self.character.vel.x
            if self.offset_x <= 0:
                self.offset_x = 0
            elif self.offset_x >= tilemap_width - WIDTH:
                self.offset_x = tilemap_width - WIDTH

        if tilemap_height <= HEIGHT:
            return
        else:
            self.offset_y = self.character.rect.centery - HEIGHT // 2

            if self.offset_y < 0:
                self.offset_y = 0
            elif self.offset_y > tilemap_height - HEIGHT:
                self.offset_y = tilemap_height - HEIGHT

    def render(self):
        # Render the level tiles and objects
        self.background.draw()
        for solid_tile in self.solid_layer:
            self.game.screen.blit(
                solid_tile.image,
                (solid_tile.rect.x - self.offset_x, solid_tile.rect.y - self.offset_y),
            )
        for platform in self.moving_platforms:
            self.game.screen.blit(
                platform.image,
                (platform.rect.x - self.offset_x, platform.rect.y - self.offset_y),
            )

        for collectable in self.collectables:
            self.game.screen.blit(
                collectable.image,
                (
                    collectable.rect.x - self.offset_x,
                    collectable.rect.y - self.offset_y,
                ),
            )
        for trap in self.traps:
            self.game.screen.blit(
                trap.image, (trap.rect.x - self.offset_x, trap.rect.y - self.offset_y)
            )

        self.game.screen.blit(
            self.goal.image,
            (
                self.goal.rect.x - self.offset_x,
                self.goal.rect.bottom - self.goal.image.get_height() - self.offset_y,
            ),
        )
        
        self.game.screen.blit(
            self.character.image,
            (
                self.character.rect.x - self.offset_x,
                self.character.rect.y - self.offset_y,
            ),
        )

        for heart in self.healthbar.hearts:
            self.game.screen.blit(heart.image, heart.rect)
