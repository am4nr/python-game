from scripts.GameObjects.gameobject import GameObject

class Collectable(GameObject):
    def init(self,game,x,y):
        self.game = game
        self.x = x
        self.y = y