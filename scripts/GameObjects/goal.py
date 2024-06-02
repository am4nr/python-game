from scripts.GameObjects.gameobject import GameObject

class Goal(GameObject):
    def init(self,game,x,y,surf,rect):
        self.game = game
        self.x = x
        self.y = y
        self.surf = surf
        self.rect = rect