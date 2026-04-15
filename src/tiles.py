import pygame.sprite
from settings import fruit_size
from support import import_cut_graphics


def rectangle_position(position_x, position_y):
    rect_list = [position_x, position_y]
    rect_list_copy = rect_list.copy()
    return rect_list_copy


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(x, y))


class StaticTileSets(Tile):
    def __init__(self, size, x, y, image):
        super().__init__(size, x, y)
        self.image = image
        self.collision_rect = pygame.Rect(self.rect.midleft, (64, 65))


class AnimatedFruits(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_cut_graphics(path, fruit_size, False, fruit_size, (-18, -15))
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # self.rect_pos = rectangle_position(self.rect.x, self.rect.y)

    def animate(self):
        self.frame_index += 0.5
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, screen_shake):
        self.animate()
        # if screen_shake == 0:
        #     self.rect.x = self.rect_pos[0]
        #     self.rect.y = self.rect_pos[1]
        # else:
        #     self.rect.x += screen_shake
        #     self.rect.y += screen_shake


class Fruits(AnimatedFruits):
    def __init__(self, size, x, y, path, surface):
        super().__init__(size, x, y, path)
        self.display_surface = surface

        # self.rect_pos = rectangle_position(self.rect.x, self.rect.y)

    def test_collision(self):
        pygame.draw.rect(self.display_surface, "red", self.rect, 1)

    def update(self, screen_shake):
        # self.test_collision()
        self.animate()
        # if screen_shake == 0:
        #     self.rect.x = self.rect_pos[0]
        #     self.rect.y = self.rect_pos[1]
        # else:
        #     self.rect.x += screen_shake
        #     self.rect.y += screen_shake


class Skull(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_cut_graphics(path, size, False, 66, (0, 0))
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.25
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
