import pygame
from scripts.settings import *
from scripts.animation import Animation
from scripts.command import RunLeft, RunRight, Jump
vec = pygame.math.Vector2

class Character():
    def __init__(self, sprites, acc, friction):
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = acc
        self.friction = friction
        self.sprites = sprites
        self.image = self.sprites["idle"][0]
        self.animation = Animation()
        self.rect = self.image.get_rect()

    def update(self):
        self.handle_Playerinput()
        self.image = self.animation.update()
        
    def handle_Playerinput(self):
        key_pressed = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            RunLeft().execute(self)
            key_pressed = True
        if keystate[pygame.K_RIGHT]:
            RunRight().execute(self)
            key_pressed = True
        
        if not key_pressed:
            self.animation.get_image(self.sprites["idle"])


