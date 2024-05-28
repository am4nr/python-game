import pygame

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.levels = []
        self.current_level = None
    
    def set_level(self, level):
        pass
    
    def next_level(self):
        pass
    
class Level:
    __levels = []
    def __init__(self, tilemap):
        self.game = LevelManager.game
        self.tilemap = self.game.assets.get("Tilemap", tilemap )
        self.tilesets = tilemap.tilesets
        self.tiles = {}
        self.gameObjects = pygame.sprite.Group()
        
        LevelManager.levels.append(self)

    def load(self):
        pass
    
    def update(self):
        self.gameObjects.update()
        
    def render(self):
        for layer in self.tilemap.get_layers().values():
            layer["group"].draw(self.game.screen)
            
        self.gameObjects.draw(self.game.screen)
