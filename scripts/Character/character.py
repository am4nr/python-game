import pygame
from scripts.Utils.settings import *
from scripts.Utils.animation import Animation
from scripts.Character.playerCommand import RunLeft, RunRight, Jump
from scripts.Character.characterMovement import VerticalMovement
from scripts.Character.characterState import CharacterState, Idle, Falling
from scripts.Utils.collision import Collision

vec = pygame.math.Vector2


class Character(pygame.sprite.Sprite):
    def __init__(self, game, sprites, acc, friction):
        self.game = game
        self.pos = vec(200, 400)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = acc
        self.friction = friction
        self.sprites = sprites
        self.animation = Animation()
        self.state = CharacterState(self)
        self.image = self.sprites["idle"][0].image
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.jumps = 2
        self.collision = Collision(self.game)
        self.direction = "right"
        self.jumping = False
        self.on_ground = False
        self.animation.get_images(self.sprites["idle"], self.direction)
        self.idle_waiting_time_counter = 0 
        self.sounds_jump = game.assets.get("Sound", "SFX/jump.wav")
        self.collided_x = False

    def update(self):
        self.image = self.animation.update()
        self.collided_x = False
        self.handle_Playerinput()
        self.gravity()
        self.collision.handle_horizontal_collision(self)
        self.collision.handle_vertical_collision(self)
        self.idle_waiting_time_counter += 1

    def gravity(self):
      
        if not self.on_ground:
            self.vel.y = GRAVITY
            self.state.changeState(Falling)
            VerticalMovement().execute(self)
            self.jumping = False
            

    def handle_Playerinput(self):
        key_pressed = False
        keystate = self.game.keystate
       
        if not self.collided_x:
            if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
                key_pressed = True
                RunLeft().execute(self)

            if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
                key_pressed = True
                RunRight().execute(self)
        else: 
            self.collided_x = False

        if keystate[pygame.K_SPACE] and self.jumps > 0:
            key_pressed = True
            Jump().execute(self)

        if not key_pressed and self.on_ground and self.idle_waiting_time_counter >= 12:
            self.state.changeState(Idle)
            self.idle_waiting_time_counter = 0