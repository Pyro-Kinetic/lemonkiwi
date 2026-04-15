import pygame
from support import import_folder
from support import import_cut_graphics
from settings import collected_size


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.25
        if animation_type == 'jump':
            self.frames = import_folder('../graphics/main_characters/dust_particles/jump')
        if animation_type == 'land':
            self.frames = import_folder('../graphics/main_characters/dust_particles/land')

        if animation_type == "collected":
            self.frames = import_cut_graphics(path="../graphics/items/fruits/collected.png",
                                              tile_size=collected_size, is_tile_on_y_axis=False,
                                              offset_y=collected_size,
                                              destination=(0, 0))
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
