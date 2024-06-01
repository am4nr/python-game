import pygame
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
        if index == len(self.levels)-1:
            self.current_level = self.levels[0]
            self.game.character.collision.update_level()
        else:
            self.current_level = self.levels[index+1]
            self.game.character.collision.update_level()
        
    def load_levels(self):         #⬇️, "Test-Level2"
        for level_name in ["Test-Level"]:
            if len(self.levels) == 0:
                self.current_level = Level(self.game, level_name, len(self.levels))
                self.levels.append(self.current_level)
            else:
                self.levels.append(Level(self.game, level_name, len(self.levels)))


                
class Level:
    def __init__(self, game, level_name, level_id):
        self.game = game
        self.tilemap = game.assets.get("Tilemap", level_name)
        self.tilesets = self.tilemap.tilesets
        self.tiles = {}
        self.gameObjects = pygame.sprite.Group()
        self.levelObjects = []
        self.id = level_id
        self.moving_platforms = []
        self.load()

    def load(self):
        self.tilemap.load_layers()
        self.moving_platforms = self.tilemap.layers["gameObjects"]["moving_platforms"]
        print(f"Loaded {len(self.moving_platforms)} moving platforms")
        for platform in self.moving_platforms:
            print(f"Loaded platform: {platform}")
            self.gameObjects.add(platform.sprite)  # Add the platform sprite to the gameObjects group


    def update(self):
        #print("Updating level")
        self.gameObjects.update()
        for platform in self.moving_platforms:
            print(f"Updating platform: {platform}")
            platform.update()

    def render(self):
        #print("render level")
        # Render the level tiles and objects
        for layer in self.tilemap.get_layers().values():
            layer["group"].draw(self.game.screen)
        print(self.moving_platforms)
        for platform in self.moving_platforms:
            platform.draw(self.game.screen)
            
        """ for obj in self.gameObjects:
            obj.draw(self.game.screen) """