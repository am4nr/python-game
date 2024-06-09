from scripts.GameObjects.gameobject import GameObject
from scripts.Utils.animation import Animation


class Goal(GameObject):
    def __init__(self, game, x, y):
        self.game = game
        super().__init__(game)
        self.x = x - 12
        self.y = y + 12
        self.collided = False
        self.state = "sleep"

    def load(self):
        if self.game.level_manager.current_level.character.name == "finn":
            self.sprites = self.game.sprites.handle_spritesheetDictTransformation(
                self.game.sprites.get_spritesheets("goal", "quack"), 64, 64, 1
            )
        elif self.game.level_manager.current_level.character.name == "quack":
            self.sprites = self.game.sprites.handle_spritesheetDictTransformation(
                self.game.sprites.get_spritesheets("goal", "finn"), 200, 200, 0.32
            )

        self.animation = Animation()
        self.animation.get_img_dur(18)
        self.animation.get_images(self.sprites["sleep"], "left")
        self.image = self.sprites["sleep"][0].image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

        

    def update(self):
        self.image = self.animation.update()
        self.check_state()

    def handle_collision(self):
        if self.goal.state == "active":
            print("yay")

    def check_state(self):
        if self.game.level_manager.current_level.collectables.__len__() == 0:
            self.animation.reset(self.sprites["active"], "left")
            self.state = "active"