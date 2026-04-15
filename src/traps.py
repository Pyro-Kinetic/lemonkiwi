import pygame
from support import import_cut_graphics
from settings import tile_size, trampoline_size


class TrapTiles(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(x, y))


class StaticTraps(TrapTiles):
    def __init__(self, size, x, y, image):
        super().__init__(size, x, y)
        self.image = image


class Fire(StaticTraps):
    def __init__(self, size, x, y, image, offset, surface):
        super().__init__(size, x, y, image)
        offset_y = y - offset
        self.display_surface = surface
        self.rect = self.image.get_rect(topleft=(x, offset_y))
        self.collision_rect = pygame.Rect(self.rect.midleft, (64, 65))


class AnimateFireTraps(pygame.sprite.Sprite):
    def __init__(self, pos, animation_type):
        super().__init__()
        self.is_flame_on = False

        # timer setup
        self.sprite_alive = False
        self.sprite_alive_duration = 2000
        self.sprite_alive_time = 0

        # animation
        self.frame_index = 0
        self.animation_speed = 0.2
        if animation_type == "fire_hit":
            self.frames = import_cut_graphics(path="../graphics/traps/fire/hit.png",
                                              tile_size=tile_size, is_tile_on_y_axis=False, offset_y=128,
                                              destination=(0, 0))
        if animation_type == "fire_on":
            self.frames = import_cut_graphics(path="../graphics/traps/fire/on.png",
                                              tile_size=tile_size, is_tile_on_y_axis=False, offset_y=128,
                                              destination=(0, 0))
        if animation_type == "trampoline":
            self.frames = import_cut_graphics(path="../graphics/traps/trampoline/bounce.png",
                                              tile_size=tile_size, is_tile_on_y_axis=False, offset_y=128,
                                              destination=(0, 0))
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.sprite_alive_time = pygame.time.get_ticks()

    def animate(self):
        flame_on = import_cut_graphics(path="../graphics/traps/fire/on.png",
                                       tile_size=tile_size, is_tile_on_y_axis=False, offset_y=128, destination=(0, 0))
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.frames = flame_on
            self.frame_index = 0
            self.is_flame_on = True
        else:
            self.image = self.frames[int(self.frame_index)]
            self.is_flame_on = False

        if self.sprite_alive:
            self.kill()
            self.sprite_alive = False

    def flame_on_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.sprite_alive_time >= self.sprite_alive_duration:
            self.sprite_alive = True

    def update(self):
        self.animate()
        self.flame_on_timer()


class Trampoline(StaticTraps):
    def __init__(self, size, x, y, image, offset_x, offset_y, surface):
        super().__init__(size, x, y, image)
        offset_y = y - offset_y
        offset_x = x - offset_x
        self.display_surface = surface
        self.rect = self.image.get_rect(topleft=(offset_x, offset_y))
        self.collision_rect = pygame.Rect(self.rect.midleft, (82, 40))


class AnimateTrampoline(pygame.sprite.Sprite):
    def __init__(self, pos, animation_type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.45

        if animation_type == "bounce":
            self.frames = import_cut_graphics(path="../graphics/traps/trampoline/bounce.png", tile_size=trampoline_size,
                                              is_tile_on_y_axis=False, offset_y=trampoline_size, destination=(0, 0))
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
