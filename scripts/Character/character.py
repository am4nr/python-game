import pygame
from scripts.Utils.settings import *
from scripts.Utils.animation import Animation
from scripts.Character.playerCommand import RunLeft, RunRight, Jump, NoInput
from scripts.Character.characterMovement import VerticalMovement
from scripts.Character.characterState import CharacterState, Idle, RunningLeft, RunningRight, Jumping, Falling, Landing
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


    def update(self):
        self.image = self.animation.update()
        self.state.update()
        self.collision.resolve_horizontal_collision(self)
        self.collision.resolve_vertical_collision(self)
        self.handle_playerinput() 
        self.gravity()

    def gravity(self):
        if not self.on_ground and not self.jumping:
            self.state.changeState(Falling)    
            VerticalMovement().execute(self)
            

    def handle_playerinput(self):
        key_pressed = False
        keystate = self.game.keystate

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            key_pressed = True
            RunLeft().execute(self)

        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            key_pressed = True
            RunRight().execute(self)

        if keystate[pygame.K_SPACE]:
            key_pressed = True
            Jump().execute(self)

        if not key_pressed: 
            NoInput().execute(self)