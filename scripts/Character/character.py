import pygame
from scripts.Utils.animation import Animation
from scripts.Character.playerCommand import RunLeft, RunRight, Jump, NoInput
from scripts.Character.characterMovement import VerticalMovement
from scripts.Character.characterState import CharacterState, Falling 
from scripts.Utils.collision import Collision
vec = pygame.math.Vector2


class Character(pygame.sprite.Sprite):
    def __init__(self, name, tilesize, scale, speed, gravity, friction):
        self.game = None
        self.name = name
        self.tilesize = tilesize
        self.scale = scale
        self.pos = None
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = speed
        self.gravity = gravity
        self.friction = friction
        self.state = CharacterState(self)   
        self.jumps = 2
        self.direction = "right"
        self.jumping = False
        self.on_ground = False
        self.idle_waiting_time_counter = 0
        self.collided_x = False
        self.collided_y = False
        

    def load(self):
        self.sprites = self.game.sprites.handle_spritesheetDictTransformation(
            self.game.sprites.get_spritesheets("characters", self.name),
            self.tilesize,
            self.tilesize,
            self.scale
        )
        self.animation = Animation()
        self.animation.get_images(self.sprites["idle"], self.direction)
        self.image = self.sprites["idle"][0].image
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.sounds_jump = self.game.assets.get("Sound", "SFX/jump.wav")
        self.collision = Collision(self.game)
        
        
    def update(self):
        self.image = self.animation.update()
        self.state.update()
        self.key_pressed = False
        self.collision.vertical_collision(self)
        self.collision.horizontal_collision(self)
        self.collision.object_collision(self)
        self.horizontal_move()
        self.apply_gravity()
        self.jump()
        self.handle_idle()

    def apply_gravity(self):
        if not self.on_ground and not self.jumping:
            VerticalMovement().execute(self)
            self.state.changeState(Falling)

    def jump(self):
        for event in self.game.events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.key_pressed = True
                    if self.jumps > 0:
                        self.jumping = True
                        Jump().execute(self)

    def horizontal_move(self):
        keystate = self.game.keystate

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.key_pressed = True
            self.direction = "left"
            RunLeft().execute(self)

        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.key_pressed = True
            self.direction = "right"
            RunRight().execute(self)

    def handle_idle(self):
        if not self.key_pressed:
            NoInput().execute(self)
