import pygame
from scripts.settings import *
from scripts.animation import Animation
from scripts.playerCommand import RunLeft, RunRight, Jump
from scripts.characterMovement import VerticalMovement
from scripts.characterState import CharacterState, Idle
from scripts.collision import Collision

vec = pygame.math.Vector2


class Character(pygame.sprite.Sprite):
    def __init__(self, game, sprites, acc, friction):
        self.game = game
        self.pos = vec(CHARACTER_START_POS_X, CHARACTER_START_POS_Y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = acc
        self.friction = friction
        self.sprites = sprites
        self.animation = Animation()
        self.state = CharacterState(self)
        self.image = self.sprites["idle"][0].image
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # self.rect.left = CHARACTER_START_POS_X
        # self.rect.bottom = CHARACTER_START_POS_Y
        self.jumps = 2
        self.animation.get_images(self.sprites["idle"], False)
        self.collision = Collision(self.game)
        self.dircetion = "right"

    def update(self):
        self.gravity()
        self.image = self.animation.update()
        # self.mask = pygame.mask.from_surface(self.image)
        # self.collision.handle_vertical_collision(self)
        self.handle_Playerinput()
        print(self.pos.y, self.rect.y, self.rect.bottom)

    def gravity(self):

        if not self.collision.handle_vertical_collision(self):
            self.vel.y = GRAVITY
            VerticalMovement().execute(self)
        #temporary handle screen boundaries
        # if self.rect.bottom > HEIGHT:
        #     self.rect.bottom = HEIGHT
        #     self.acc.y = 0

    def handle_Playerinput(self):
        key_pressed = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            key_pressed = True
            # self.direction = 'left'
            RunLeft().execute(self)

        if keystate[pygame.K_RIGHT]:
            key_pressed = True
            # self.direction = 'right'
            RunRight().execute(self)

        if keystate[pygame.K_SPACE] and self.jumps > 0:
            key_pressed = True
            self.vel.y = -GRAVITY * 60
            self.jumps -= 1
            Jump().execute(self)

        # add falling
        # if not key_pressed:
        #     self.state.changeState(Idle)
