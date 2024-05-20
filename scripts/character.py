import pygame
from scripts.settings import *
from scripts.animation import Animation
from scripts.playerCommand import RunLeft, RunRight, Jump
from scripts.characterMovement import VerticalMovement
from scripts.characterState import CharacterState, Idle

vec = pygame.math.Vector2


class Character(pygame.sprite.Sprite):
    def __init__(self, sprites, acc, friction):
        self.pos = vec(CHARACTER_START_POS_X, CHARACTER_START_POS_Y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = acc
        self.friction = friction
        self.sprites = sprites
        self.animation = Animation()
        self.state = CharacterState(self)
        self.image = self.sprites["idle"][0].image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()
        self.rect.left = CHARACTER_START_POS_X
        self.rect.bottom = CHARACTER_START_POS_Y
        self.jumps = 2
        self.animation.get_images(self.sprites["idle"], False)

    def update(self):
        self.gravity()
        self.handle_Playerinput()
        self.image = self.animation.update()
        self.mask = pygame.mask.from_surface(self.image)

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
            self.vel.y = -GRAVITY * 60
            self.jumps -= 1
            Jump().execute(self)

        # add falling
        # if not key_pressed:
        #     self.state.changeState(Idle)
