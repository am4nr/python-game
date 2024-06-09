from scripts.Utils.animation import Animation
import pygame
vec = pygame.math.Vector2

class Healthbar():
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.hearts = []

    def load(self):
        #print(self.game)
        for i in range (self.game.level_manager.current_level.character.health):
            self.hearts.append(Heart(self.game, self.x + i * 23, self.y))

    def update(self):
        for heart in self.hearts:
            if heart.animation.check_done:
                heart.image = heart.sprites["heart_full"][4].image
            else:
                heart.image = heart.animation.update()
        # self.rect = self.image.get_rect(center=(self.x,self.y))
        pass

class Heart():
    def __init__(self, game, x, y):
        self.game = game
        self.sprites = game.sprites.handle_spritesheetDictTransformation(
            game.sprites.get_spritesheets("objects", "Hearts"),
            20,
            18
        )
        self.x = x
        self.y = y
        self.animation = Animation()
        self.animation.get_img_dur(6)
        self.animation.get_surfaces(self.sprites["heart_full"])
        self.image = self.sprites["heart_full"][0].image
        self.rect = self.image.get_rect(center=(self.x,self.y))

    def update(self):
        pass

    def deplete(self):
        self.animation.reset(self.sprites["heart_deplete"], "right", False, 6)