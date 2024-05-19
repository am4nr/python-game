from scripts.characterMovement import CharacterRun, CharacterJump
import pygame


class Context:
    def __init__(self, character):
        self.character = character
        self.currentState = Idle

    def interface(self):
        self.currentState.interface()
    def changeState(self, newState):
        if (self.currentState != newState): 
            self.currentState = newState
            self.currentState.enter(self)
            # self.currentState.exit()

    def update(self):
        pass

class Idle(Context):
    def __init__(self, character):
        self.character = character

    def enter(self):
        self.character.animation.reset(self.character.sprites["idle"])


class RunningRight(Context):
    def __init__(self, character):
        self.character = character

    def enter(self):
        CharacterRun().accelerate(0,self.character, False)
        self.character.animation.reset(self.character.sprites["run"])

    def update(self):
        CharacterRun().execute(self.character, False)


class RunningLeft(Context):
    def __init__(self, character):
        self.character = character

    def enter(self):
        CharacterRun().execute(self.character, True)
        flippedSprites = []
        for sprite in self.character.sprites["run"]:
           flippedSprites.append(pygame.transform.flip(sprite, True, False))
        self.character.animation.reset(flippedSprites)


# class Jumping(CharacterContext):
#     def enter(self, character, mirror):
#         self.currentState = "jump"
#         CharacterJump().execute(character, mirror)

# class Falling(CharacterState):
#     def enter(self, character, mirror):
#         self.currentState = "jump"
#         CharacterJump().execute(character, mirror)