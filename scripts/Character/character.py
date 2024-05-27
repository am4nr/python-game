import pygame
from scripts.Utils.settings import *
from scripts.Utils.animation import Animation
from scripts.Character.playerCommand import RunLeft, RunRight, Jump
from scripts.Character.characterMovement import VerticalMovement
from scripts.Character.characterState import CharacterState, Idle
from scripts.Utils.collision import Collision

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
        #self.rect.bottom = self.pos[1]
        # self.rect.left = CHARACTER_START_POS_X
        # self.rect.bottom = CHARACTER_START_POS_Y
        self.jumps = 2
        self.animation.get_images(self.sprites["idle"], False)
        self.collision = Collision(self.game)
        self.direction = "right"
        self.on_ground = False

    def update(self):
        self.image = self.animation.update()
        #self.rect.bottom = self.pos[1]
        self.collision.handle_vertical_collision(self)
        self.gravity()
        self.handle_Playerinput()
        # self.mask = pygame.mask.from_surface(self.image)
        self.collision.handle_vertical_collision(self)
        #print(self.pos.y, self.rect.y, self.rect.bottom)

    def gravity(self):

        if not self.on_ground:
            self.vel.y = GRAVITY
            VerticalMovement().execute(self)
        #temporary handle screen boundaries
        # if self.rect.bottom > HEIGHT:
        #     self.rect.bottom = HEIGHT
        #     self.acc.y = 0

    def handle_Playerinput(self):
        key_pressed = False
        keystate = self.game.keystate
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            key_pressed = True
            # self.direction = 'left'
            RunLeft().execute(self)

        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
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
