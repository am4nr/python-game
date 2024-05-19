import pygame
from scripts.settings import *
from scripts.animation import Animation
from scripts.playerCommand import RunLeft, RunRight
from scripts.characterMovement import CharacterFall
from scripts.characterState import Context, Idle
vec = pygame.math.Vector2

class Character():
    def __init__(self, sprites, acc, friction):
        self.pos = vec(CHARACTER_START_POS_X, CHARACTER_START_POS_Y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = acc
        self.friction = friction
        self.sprites = sprites
        self.image = self.sprites["idle"][0]
        self.animation = Animation(self.sprites["idle"])
        self.rect = self.image.get_rect()
        self.state = Context(self)
        # self.jump_count = 10

    def update(self):
        # self.gravity()
        self.handle_Playerinput()
        self.image = self.animation.update()
        
    
    # def gravity(self):
    #     if self.state != 'jump':
    #         CharacterFall().execute(self, False)
    #         #temporary handle screen boundaries
    #         if self.rect.bottom > HEIGHT:
    #             self.rect.bottom = HEIGHT
    #             self.pos.y = HEIGHT
    #             self.acc.y = 0
        
    def handle_Playerinput(self):
        key_pressed = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            key_pressed = True
            RunLeft().execute(self)
            
        if keystate[pygame.K_RIGHT]:
            key_pressed = True
            RunRight().execute(self)
            
        # if keystate[pygame.K_SPACE]:
        #     key_pressed = True
        #     if self.state != 'jump':
        #         self.state = 'jump' 
        #         self.jump_count -= 1
        #         Jump().execute(self)
        #         if self.jump_count < -10:
        #             self.state = 'fall'
        #             self.jump_count = 10
            
        
        # if not key_pressed:
        #     self.animation.get_image(self.sprites["idle"])
            # self.state = 'idle'


