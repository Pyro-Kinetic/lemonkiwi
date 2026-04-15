import sys
from csv import reader
from os import walk
from pathlib import Path

import pygame


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path_str = getattr(sys, '_MEIPASS', None)

    if base_path_str:
        base_path = Path(base_path_str)
    else:
        # In development, use the folder where THIS script is located
        base_path = Path(__file__).resolve().parent

    return str(base_path / relative_path)


def import_csv_layout(path):
    terrain_map = []
    with open(resource_path(path)) as game_map:
        level = reader(game_map, delimiter=",")
        for data in level:
            terrain_map.append(list(data))
        return terrain_map


def import_cut_graphics(path, tile_size, is_tile_on_y_axis, offset_y, destination):
    terrain_tile_set = pygame.image.load(resource_path(path)).convert_alpha()
    tile_num_x = int(terrain_tile_set.get_size()[0] / tile_size)
    tile_num_y = int(terrain_tile_set.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            if is_tile_on_y_axis:
                y = row * tile_size
            else:
                y = 0
            surface = pygame.Surface((tile_size, offset_y), flags=pygame.SRCALPHA)
            surface.blit(terrain_tile_set, destination, pygame.Rect(x, y, tile_size, offset_y))
            cut_tiles.append(surface)

    return cut_tiles


def import_folder(external_path):
    surface_list = []
    path = resource_path(external_path)

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = f"{path}/{image}"
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def image_loader(path):
    image_surf = pygame.image.load(resource_path(path)).convert_alpha()
    return image_surf


def music_loader(path):
    pygame.mixer.music.load(resource_path(path))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.09)


def sound_loader(path):
    sound = pygame.mixer.Sound(resource_path(path))
    return sound
