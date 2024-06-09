from scripts.GameObjects.gameobject import GameObject

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
        self.collision_timer = 0

    def update(self):
        pass

    def handle_collision(self):
        if self.collision_timer > 0:
            self.collision_timer -= 1
        else: 
            if self.game.level_manager.current_level.character.health > 0:
                self.game.level_manager.current_level.character.health -= 1
                print(self.game.level_manager.current_level.character.health)
                self.game.level_manager.current_level.healthbar.hearts[
                    self.game.level_manager.current_level.character.health
                ].deplete()
                self.collision_timer = 20
            else:
                print("game over")