from scripts.Utils.settings import *


class CharacterState:
    def __init__(self, character):
        self.currentState = Idle
        self.character = character

    def enter(self):
        pass

    def update(self):
        self.currentState.update(self)

    def exitState(self):
        pass

    def changeState(self, newState):
        if self.currentState != newState:
            self.currentState.exitState(self)
            self.currentState = newState
            self.currentState.enter(self)
        return self.currentState


class Idle(CharacterState):
    def enter(self):
        self.character.animation.reset(
            self.character.sprites["idle"], self.character.direction
        )
        self.character.idle_waiting_time_counter = 0

    def update(self):
        pass

    def exitState(self):
        self.character.idle_waiting_time_counter = 0


class RunningRight(CharacterState):
    def enter(self):
        self.character.vel.x = 0
        if self.character.on_ground:
            self.character.animation.reset(
                self.character.sprites["run"], self.character.direction
            )
            self.counter = 0

    def update(self):
        if self.character.on_ground and self.counter % 15 == 0:
            self.character.sounds["run"].play()
        self.counter += 1

    def exitState(self):
        self.character.vel.x = 0
        self.counter = 0


class RunningLeft(CharacterState):
    def enter(self):
        self.character.vel.x = 0
        if self.character.on_ground:
            self.character.animation.reset(
                self.character.sprites["run"], self.character.direction
            )
        self.counter = 0

    def update(self):
        if self.character.on_ground and self.counter % 15 == 0:
            self.character.sounds["run"].play()
        self.counter += 1

    def exitState(self):
        self.character.vel.x = 0
        self.counter = 0


class Jumping(CharacterState):
    def enter(self):
        self.character.vel.y = -self.character.gravity * 50
        self.character.jumps -= 1
        self.character.animation.reset(
            self.character.sprites["jump"], self.character.direction, False, 10
        )
        self.character.sounds["jump"].play()

    def update(self):
        if self.character.animation.check_done():
            self.character.state.changeState(Falling)

    def exitState(self):
        self.character.jumping = False


class Falling(CharacterState):
    def enter(self):
        self.character.vel.y = self.character.gravity
        self.character.animation.reset(
            self.character.sprites["fall"], self.character.direction
        )

    def update(self):
        if self.character.on_ground:
            self.character.state.changeState(Landing)

    def exitState(self):
        self.character.vel.y = 0


class Landing(CharacterState):
    def enter(self):
        self.character.animation.reset(
            self.character.sprites["land"], self.character.direction, False
        )
        self.character.sounds["land"].play()

    def update(self):
        if self.character.animation.check_done():
            self.character.state.changeState(Idle)

    def exitState(self):
        pass


class Hit(CharacterState):
    def enter(self):
        self.character.hit = True
        self.character.animation.reset(
            self.character.sprites["hit"], self.character.direction, False, 15
        )
        self.character.sounds["hit"].play()

    def update(self):
        if self.character.animation.check_done():
            self.character.state.changeState(Idle)

    def exitState(self):
        self.character.hit = False
        self.character.health -= 1
        self.character.game.level_manager.current_level.healthbar.hearts[
            self.character.health
        ].deplete()
