import pygame
from scripts.settings import *
from scripts.animation import Animation
from scripts.command import RunLeft, RunRight, Jump
vec = pygame.math.Vector2

class Character():
    def __init__(self, sprites, x, y, acc, friction):
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = acc
        self.friction = friction
        self.sprites = sprites
        self.image = self.sprites["idle_alt"][0]
        self.animation = Animation(self.sprites["idle_alt"])
        self.rect = self.image.get_rect()

    def update(self):
        self.image = self.animation.update()
        self.doAction()

    def doAction(self):
        key_pressed = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            RunLeft().execute(self)
            key_pressed = True
        if keystate[pygame.K_RIGHT]:
            RunRight().execute(self)
            key_pressed = True
        
        if not key_pressed:
            self.animation.change_image(self.sprites["idle_alt"])


