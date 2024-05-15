# from scripts.player import Player

class Command():
    def __init__(self, gameObject):
        self.gameObject = gameObject

    def execute(self):
        pass

class MoveLeft(Command):
    def execute(self):
        if self.vel_x < self.max_vel_x:
            self.rect.x -= self.vel_x
            self.vel_x += self.acl_x
        elif self.vel_x >= self.max_vel_x:
            self.rect.x -= self.max_vel_x

class MoveRight(Command):
    def execute(self):
        if self.vel_x < self.max_vel_x:
            self.rect.x += self.vel_x
            self.vel_x += self.acl_x
        elif self.vel_x >= self.max_vel_x:
            self.rect.x += self.max_vel_x

class Jump(Command):
    def execute(self):
        pass