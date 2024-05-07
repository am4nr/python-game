from scripts.player import Player

class PlayerCommand():
    def __init__(self, player: Player):
        self.player = player

    def execute(self):
        pass

class PlayerMoveLeft(PlayerCommand):
    def execute(self):
        self.player.move_left()

class PlayerMoveRight(PlayerCommand):
    def execute(self):
        self.player.move_right()

class PlayerJump(PlayerCommand):
    def execute(self):
        self.player.jump()