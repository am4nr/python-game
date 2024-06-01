import pygame
from scripts.Utils.animation import Animation
from scripts.Character.playerCommand import RunLeft, RunRight, Jump, NoInput
from scripts.Character.characterMovement import VerticalMovement
from scripts.Character.characterState import (
    CharacterState,
    Idle,
    RunningLeft,
    RunningRight,
    Jumping,
    Falling,
    Landing,
)
from scripts.Utils.collision import Collision

vec = pygame.math.Vector2


class Character(pygame.sprite.Sprite):
    def __init__(self, game, sprites, start_pos_x, start_pos_y, speed, friction):
        self.game = game
        self.pos = vec(start_pos_x, start_pos_y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = speed
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
        # self.dx = 0
        # self.dy = 0
        self.collided_x = False
        self.collided_y = False

    def update(self):
        # self.dx = 0
        # self.dy = 0
        self.image = self.animation.update()
        # self.rect.update(
        #     (self.rect.x, self.rect.bottom - self.image.get_height()),
        #     self.image.get_size(),
        # )
        self.state.update()
        self.key_pressed = False
        self.collision.vertical_collision(self)
        self.collision.horizontal_collision(self)
        self.gravity()
        self.jump()
        self.horizontal_move()
        # self.update_x_position()
        # self.update_y_position()
        self.handle_idle()

    def gravity(self):
        if not self.on_ground and not self.jumping:
            self.state.changeState(Falling)
            VerticalMovement().execute(self)

    def jump(self):
        for event in self.game.events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.key_pressed = True
                    Jump().execute(self)

    def horizontal_move(self):
        keystate = self.game.keystate

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.key_pressed = True
            RunLeft().execute(self)

        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.key_pressed = True
            RunRight().execute(self)

    # def update_x_position(self):
    #     DoHorizontalMovement().execute(self)

    # def update_y_position(self):
    #     DoVerticalMovement().execute(self)

    def handle_idle(self):
        if not self.key_pressed:
            NoInput().execute(self)
