import pygame
from scripts.settings import *
from scripts.animation import Animation
from scripts.playerCommand import RunLeft, RunRight, Jump
from scripts.characterMovement import VerticalMovement
from scripts.characterState import Idle
vec = pygame.math.Vector2

class Character():
    def __init__(self, sprites, acc, friction):
        self.pos = vec(CHARACTER_START_POS_X, CHARACTER_START_POS_Y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = acc
        self.friction = friction
        self.sprites = sprites
        self.sprite = self.sprites["idle"][0]
        self.animation = Animation(self.sprites["idle"])
        self.rect = self.sprite.get_rect()
        self.state = Idle.enter(self)
        self.jumps = 2
        self.mask = pygame.mask.from_surface(self.sprite)
        self.mirror = False

    def update(self):
        self.gravity()
        self.handle_Playerinput()
        self.sprite = self.animation.update()
        self.mask = pygame.mask.from_surface(self.sprite)

    def gravity(self):
        self.vel.y = GRAVITY
        VerticalMovement().execute(self, False)
        #temporary handle screen boundaries
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.pos.y = HEIGHT
            self.acc.y = 0
        
    def handle_Playerinput(self):
        key_pressed = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            key_pressed = True
            RunLeft().execute(self)
            
        if keystate[pygame.K_RIGHT]:
            key_pressed = True
            RunRight().execute(self)
            
        if keystate[pygame.K_SPACE] and self.jumps > 0:
            key_pressed = True
            self.vel.y = -GRAVITY * 8
            self.jumps -= 1
            Jump().execute(self)
            
        
        #add falling
        if not key_pressed:
            self.state.changeState(Idle)

