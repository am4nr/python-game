import pygame
from scripts.Utils.settings import *
from scripts.Utils.animation import Animation
from scripts.Character.playerCommand import RunLeft, RunRight, Jump
from scripts.Character.characterMovement import VerticalMovement
from scripts.Character.characterState import CharacterState, Idle, inAir
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
        self.rect.left = CHARACTER_START_POS_X
        self.rect.bottom = CHARACTER_START_POS_Y
        self.jumps = 2
        self.collision = Collision(self.game)
        self.direction = "right"
        self.jumping = False
        self.on_ground = False
        self.animation.get_images(self.sprites["idle"], self.direction)
        self.idle_waiting_time_counter = 0 
        self.sounds_jump = game.assets.get("Sound", "SFX/jump.wav")

    def update(self):
        #print(self.rect.x,self.rect.y)
        self.image = self.animation.update()
        #self.rect.bottom = self.pos[1]
        self.collision.handle_vertical_collision(self)
        self.gravity()
        self.handle_Playerinput()
        # self.mask = pygame.mask.from_surface(self.image)
        # self.collision.handle_vertical_collision(self)
        self.idle_waiting_time_counter += 1

    def gravity(self):

        if not self.on_ground:
            self.vel.y = GRAVITY
            self.state.changeState(inAir)
            VerticalMovement().execute(self)
            self.jumping = False
            



    def handle_Playerinput(self):
        key_pressed = False
        keystate = self.game.keystate
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            if self.collision.handle_horizontal_collision(self):
                key_pressed = True
                RunLeft().execute(self)

        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            if self.collision.handle_horizontal_collision(self):
                key_pressed = True
                RunRight().execute(self)

        if keystate[pygame.K_SPACE] and self.jumps > 0:
            key_pressed = True
            # self.vel.y = -GRAVITY * 60
            # self.jumps -= 1
            self.sounds_jump.play()
            Jump().execute(self)

        if not key_pressed and self.on_ground and self.idle_waiting_time_counter >= 12:
            self.state.changeState(Idle)
            self.idle_waiting_time_counter = 0
