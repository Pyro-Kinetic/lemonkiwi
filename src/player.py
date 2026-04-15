import pygame
from tiles import Tile
from settings import tile_size
from support import import_folder
from support import import_cut_graphics, sound_loader


class Player(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.frames = None
        self.dust_run_particles = None
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.3
        self.image = self.frames["idle.png"][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        # audio
        self.jump_sound1 = sound_loader("../audio/jump.mp3")

        # pygame timer
        self.current_time = 0
        self.button_press_time = 0

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.2
        self.display_surface = surface

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_height = -14
        self.jump_counter = 0
        self.collision_rect = pygame.Rect(self.rect.topleft, (35, 55))
        self.wall_slide_rect = pygame.Rect(self.rect.topleft, (37, 55))

        # player status
        self.status = "idle.png"
        self.facing_right = True
        self.facing_left = False
        self.on_ground = False
        self.on_wall = False
        self.on_left_wall = False
        self.on_right_wall = False
        self.hit = False

    def import_character_assets(self):
        character_path = "../graphics/main_characters/virtual_guy/"
        self.frames = {
            "double_jump.png": [],
            "fall.png": [],
            "hit.png": [],
            "hit_red.png": [],
            "idle.png": [],
            "jump.png": [],
            "run.png": [],
            "wall_jump.png": []
        }

        for frame in self.frames.keys():
            full_path = character_path + frame
            self.frames[frame] = import_cut_graphics(path=full_path, tile_size=tile_size, is_tile_on_y_axis=False,
                                                     offset_y=tile_size, destination=(0, 0))

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder("../graphics/main_characters/dust_particles/run")

    def test_sprite_rect(self):
        pygame.draw.rect(self.display_surface, "green", self.rect, 1)

    def test_collision_rect(self):
        pygame.draw.rect(self.display_surface, "red", self.collision_rect, 1)

    def test_wall_slide_rect(self):
        pygame.draw.rect(self.display_surface, "blue", self.wall_slide_rect, 1)

    def animate(self):
        self.rect.midbottom = self.collision_rect.midbottom
        # self.rect.center = pygame.mouse.get_pos()
        self.wall_slide_rect.midbottom = self.collision_rect.midbottom
        animation = self.frames[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        flipped_image = pygame.transform.flip(image, True, False)
        if self.facing_right:
            self.image = image
        else:
            self.image = flipped_image

    def run_dust_animation(self):
        if self.status == "run.png" and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.collision_rect.bottomleft - pygame.math.Vector2(20, 12)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.collision_rect.bottomright - pygame.math.Vector2(-5, 12)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if self.on_left_wall and keys[pygame.K_RIGHT]:
            self.direction.y = self.jump_height
            self.jump_sound1.play()
        elif self.on_right_wall and keys[pygame.K_LEFT]:
            self.direction.y = self.jump_height
            self.jump_sound1.play()
        else:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing_right = True

            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing_right = False
            else:
                self.direction.x = 0

    def get_status(self):
        if self.direction.y == -31:
            self.hit = True
        elif self.hit:
            self.status = "hit_red.png"
        elif self.direction.y == 2:
            self.status = "wall_jump.png"
            self.on_wall = True
        elif self.direction.y > 0:
            self.status = "fall.png"
        elif self.jump_counter == 2:
            self.status = "double_jump.png"
        elif self.direction.y < 0:
            self.status = "jump.png"
        else:
            self.on_wall = False
            if self.direction.x != 0:
                self.status = "run.png"
            else:
                self.status = "idle.png"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_height
        self.jump_counter += 1

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        # self.test_sprite_rect()
        # self.test_collision_rect()
        # self.test_wall_slide_rect()
