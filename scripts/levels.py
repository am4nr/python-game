class Levels:
    def __init__(self, game, tilemap):
        self.game
        self.tilemap = tilemap
        self.tilesets = tilemap.tilesets
        self.tiles = {}

    def draw(self):
        for tile in self.tiles:
            self.game.screen.blit(tile[0], tile[1])
