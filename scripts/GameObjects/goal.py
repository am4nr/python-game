from scripts.GameObjects.gameobject import GameObject
from scripts.Utils.animation import Animation


class Goal(GameObject):
    def __init__(self,game,x,y):
        self.game = game
        super().__init__(game)
        self.x = x
        self.y = y

        self.sprites = game.sprites.handle_spritesheetDictTransformation(
            game.sprites.get_spritesheets("objects", "Arrow"),
            18,
            18,
        )
        self.animation = Animation()
        self.animation.upsidedown(self.sprites["Idle"])
        self.image = self.sprites["Idle"][0].image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collided = False

    def update(self):
        self.image = self.animation.update()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def handle_collision(self):
        self.animation.upsidedown(self.sprites["Hit"])
        self.game.level_manager.current_level.check_goal()
