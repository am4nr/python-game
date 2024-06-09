import pygame
from scripts.Character.characters import Finn, Quack
from scripts.Utils.settings import WIDTH
from scripts.GameObjects.collectable import Collectable

vec = pygame.math.Vector2
levels = [
    {"level_name": "Test-Level", "character": Quack},
    {"level_name": "Test-Level2", "character": Finn},
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
            character.game = self.game
            if len(self.levels) == 0:
                self.current_level = Level(
                    self.game, level_name, len(self.levels), character
                )
                self.levels.append(self.current_level)
            else:
                self.levels.append(
                    Level(self.game, level_name, len(self.levels), character)
                )


class Level:
    def __init__(self, game, level_name, level_id, character):
        self.game = game
        self.tilemap = game.assets.get("Tilemap", level_name)
        self.tilesets = self.tilemap.tilesets
        self.tiles = {}
        self.gameObjects = pygame.sprite.Group()
        self.levelObjects = []
        self.id = level_id
        self.moving_platforms = []
        self.character = character
        self.offset = 0

    def load(self):
        # if self.solid_layer:
        #     del self.solid_layer
        self.gameObjects = pygame.sprite.Group()
        self.tilemap.load_layers()
        self.moving_platforms = self.tilemap.layers["gameObjects"]["moving_platforms"]
        self.solid_layer = self.tilemap.layers["solid"]["group"]
        for platform in self.moving_platforms:
            self.solid_layer.add(
                platform
            )  # Add the platform sprite to the gameObjects group
        self.gameObjects.add(self.tilemap.layers["gameObjects"]["group"])
        self.character.pos = vec(200, 200)
        self.character.load()
        # self.character.collision.update_level()

    def update(self):
        # self.character.collision.update_level()
        # print("Updating level")
        self.gameObjects.update()
        for platform in self.moving_platforms:
            # print(f"Updating platform: {platform}")
            platform.update()
        self.character.update()
        self.set_offset()
        if self.gameObjects.has(Collectable):
            print("got")
        

    def set_offset(self):
        # if (
        #     (self.tilemap.width * self.tilemap.tile_width) > WIDTH
        # ) and self.character.pos.x > WIDTH / 2:
        #     self.offset = self.character.pos.x - WIDTH / 2
        # else:
        #     self.offset = 0
        
        scroll_area_width = WIDTH * 0.2
        tilemap_width = self.tilemap.width * self.tilemap.tile_width
        if tilemap_width <= WIDTH:
            return
        elif (
            (self.character.rect.right - self.offset >= WIDTH - scroll_area_width)
            and self.character.vel.x > 0
        ) or (
            (self.character.rect.left - self.offset <= scroll_area_width)
            and self.character.vel.x < 0
        ):
            self.offset += self.character.vel.x
            if self.offset <=0:
                self.offset = 0
            elif self.offset >=  tilemap_width-WIDTH:
                self.offset = tilemap_width-WIDTH

    def check_goal(self):
        #update only Collectable

        if self.gameObjects.__len__() == 0:
            print("yay")

    def render(self):
        # print("render level")
        # Render the level tiles and objects
        for solid_tile in self.solid_layer:
            self.game.screen.blit(
                solid_tile.image, (solid_tile.rect.x - self.offset, solid_tile.rect.y)
            )
        # self.solid_layer.draw(self.game.screen)
        # for layer in self.tilemap.get_layers().values():
        #     layer["group"].draw(self.game.screen)
        # print(self.moving_platforms)
        for platform in self.moving_platforms:
            self.game.screen.blit(
                platform.image, (platform.rect.x - self.offset, platform.rect.y)
            )
            # platform.blit(self.game.screen)

        for gameObject in self.gameObjects:
            self.game.screen.blit(
                gameObject.image, (gameObject.rect.x - self.offset, gameObject.rect.y)
            )
        # self.gameObjects.draw(self.game.screen)
        self.game.screen.blit(
            self.character.image,
            (self.character.rect.x - self.offset, self.character.rect.y),
        )
