from scripts.GameObjects.gameobject import GameObject
from scripts.Character.characterState import Hit

class Trap(GameObject):
    def __init__(self,game,x,y):
        self.game = game
        super().__init__(game)
        self.x = x
        self.y = y + 32
        self.collided = False
        self.sprites = game.sprites.handle_spritesheetDictTransformation(
            game.sprites.get_spritesheets("objects", "Spikes"),
            16,
            16,
            1.75
        )
        self.image = self.sprites["Idle"][0].image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.x, self.y)
        self.collision_time = 0

    def update(self):
        self.collisiontimer()

    def collisiontimer(self):
        if self.collision_time > 0:
            self.collision_time -= 1
            self.collided = False

    def handle_collision(self):
        if self.game.level_manager.current_level.character.health > 0 and self.collision_time == 0:
            self.game.level_manager.current_level.character.state.changeState(Hit)
            self.collided = True
            self.collision_time = 90
