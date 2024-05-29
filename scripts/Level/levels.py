import pygame
class LevelManager:
    def __init__(self, game):
        self.game = game
        self.levels = []
        self.current_level = None

    def set_level(self, level_name):
        self.current_level = Level(level_name, self.game)
        self.current_level.load()
class Level:
    def __init__(self, level_name, game):
        self.game = game
        self.tilemap = game.assets.get("Tilemap", level_name)
        self.tilesets = self.tilemap.tilesets
        self.tiles = {}
        self.gameObjects = pygame.sprite.Group()
        self.levelObjects = []

    def load(self):
        self.tilemap.load_layers()

    def update(self):
        self.gameObjects.update()

    def render(self):
        # Render the level tiles and objects
        for obj in self.levelObjects:
            obj.render()