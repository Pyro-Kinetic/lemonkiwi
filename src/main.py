import asyncio
import sys

import pygame
from end_credits import EndCredits
from level import Level
from over_world import OverWorld
from settings import screen_width, screen_height
from support import music_loader, sound_loader, resource_path
from ui import UI


# pyinstaller --noconsole --onefile --icon="icon.ico" --add-data "audio;audio" --add-data "graphics;graphics" --add-data "levels;levels" --add-data "src;src" --add0data "32x32;32x32" src/main.py


class Game:
    def __init__(self, surface):

        self.display_surface = surface
        self.level_number = 0
        self.max_level = 5
        self.status = "over_world"
        self.over_world = OverWorld(self.display_surface, self.load_level)
        self.level = Level(self.display_surface, self.level_number, self.load_over_world)
        self.end_credits = EndCredits(self.display_surface, self.load_over_world)
        self.screen_shake = self.level.screen_shake

        # UI
        self.ui = UI(screen)
        self.fruit_surface = ""
        self.max_fruits = self.level.total_fruits

        # audio
        music_loader("../audio/upbeat_pop.wav")
        self.button_click_sound = sound_loader("../audio/button_click.mp3")
        self.button_click_sound.set_volume(0.5)
        self.level_cleared_sound = sound_loader("../audio/level_cleared.mp3")
        self.burp_sound = pygame.mixer.Sound(resource_path("../audio/burp.mp3"))

    def show_collected_fruit_amount(self):
        if self.max_fruits == "completed":
            self.fruit_surface = "cleared!"
        else:
            self.fruit_surface = f"{self.level.collected_fruits}/{self.max_fruits}"

    def load_over_world(self):
        self.over_world = OverWorld(self.display_surface, self.load_level)
        self.status = "over_world"
        self.max_fruits = 0
        self.max_fruits += self.level.total_fruits

    def load_level(self):
        self.level = Level(self.display_surface, self.level_number, self.load_over_world)
        self.status = "level"
        self.max_fruits = 0
        self.max_fruits += self.level.total_fruits

    def render_checkpoint(self):
        if self.level.collected_fruits == self.max_fruits:
            self.level.render_skull = True
            self.max_fruits = "completed"
            self.level_cleared_sound.play()

    def level_switcher_buttons(self, pygame_event):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]

        previous_button = pygame.sprite.Group.sprites(game.level.menu_sprites)[0]
        restart_button = pygame.sprite.Group.sprites(game.level.menu_sprites)[1]
        next_button = pygame.sprite.Group.sprites(game.level.menu_sprites)[2]
        over_world_button = pygame.sprite.Group.sprites(game.level.menu_sprites)[3]

        if over_world_button.rect.collidepoint(mouse_pos) and left_click:
            if pygame_event.type == pygame.MOUSEBUTTONDOWN:
                self.button_click_sound.play()
                self.load_over_world()

        if previous_button.rect.collidepoint(mouse_pos) and left_click:
            if pygame_event.type == pygame.MOUSEBUTTONDOWN and self.level_number > 0:
                self.button_click_sound.play()
                self.level_number -= 1
                self.load_level()
                self.max_fruits = 0
                self.max_fruits += self.level.total_fruits

        if restart_button.rect.collidepoint(mouse_pos) and left_click:
            if pygame_event.type == pygame.MOUSEBUTTONDOWN:
                self.button_click_sound.play()
                self.level_number += 0
                self.load_level()
                self.max_fruits = 0
                self.max_fruits += self.level.total_fruits

        if next_button.rect.collidepoint(mouse_pos) and left_click and self.level_number < self.max_level:
            if pygame_event.type == pygame.MOUSEBUTTONDOWN:
                self.button_click_sound.play()
                self.level_number += 1
                self.load_level()

                self.max_fruits = 0
                self.max_fruits += self.level.total_fruits

    def level_switcher_keys(self, pygame_event):
        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_n:
                self.button_click_sound.play()
                self.level_number += 1
                self.load_level()

                self.max_fruits = 0
                self.max_fruits += self.level.total_fruits

        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_r:
                self.button_click_sound.play()
                self.level_number += 0
                self.load_level()
                self.max_fruits = 0
                self.max_fruits += self.level.total_fruits

        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_b:
                self.button_click_sound.play()
                self.level_number -= 1
                self.load_level()
                self.max_fruits = 0
                self.max_fruits += self.level.total_fruits

    def level_switcher_number_keys(self, pygame_event):
        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_0:
                self.level_number = 0
                self.button_click_sound.play()
                self.load_level()
        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_1:
                self.level_number = 1
                self.button_click_sound.play()
                self.load_level()
        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_2:
                self.level_number = 2
                self.button_click_sound.play()
                self.load_level()
        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_3:
                self.level_number = 3
                self.button_click_sound.play()
                self.load_level()
        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_4:
                self.level_number = 4
                self.button_click_sound.play()
                self.load_level()
        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_5:
                self.level_number = 5
                self.button_click_sound.play()
                self.load_level()

    def level_cleared(self):
        if pygame.sprite.spritecollide(self.level.player.sprite, self.level.checkpoint_sprites, False,
                                       pygame.sprite.collide_rect):
            mask_collision = pygame.sprite.spritecollide(self.level.player.sprite, self.level.checkpoint_sprites,
                                                         False, pygame.sprite.collide_mask)
            if mask_collision and self.level.render_skull and self.level_number < self.max_level:
                self.burp_sound.play()

                self.level_number += 1
                self.load_level()
                self.max_fruits = 0
                self.max_fruits += self.level.total_fruits

            if mask_collision and self.level.render_skull and self.level_number == self.max_level:
                for sprite in mask_collision:
                    sprite.kill()
                pygame.mixer.music.stop()
                music_loader("../audio/over_world_music.mp3")
                self.level_cleared_sound.play()
                self.status = "end_credits"
                self.max_fruits = 0
                self.max_fruits += self.level.total_fruits
                self.level_number = 0
                self.level.collected_fruits = 0
                self.fruit_surface = f"{self.level.collected_fruits}/{self.max_fruits}"

    def run(self):
        if self.status == "over_world":
            self.over_world.run()
        elif self.status == "end_credits":
            self.end_credits.run()
        else:
            self.level.run()
            self.ui.show_fruits(self.fruit_surface)
        self.show_collected_fruit_amount()
        self.render_checkpoint()
        self.level_cleared()


# pygame setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

icon = pygame.image.load(resource_path("../graphics/logo.png"))
pygame.display.set_icon(icon)
pygame.display.set_caption("Lemon Kiwi")

fps = 60
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game(screen)


async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game.level.player_double_jump_mechanic(event)
            game.level_switcher_buttons(event)
            game.level_switcher_keys(event)
            game.level_switcher_number_keys(event)

        current_time = pygame.time.get_ticks()

        screen.fill("burlywood3")
        game.run()

        pygame.display.update()
        clock.tick(fps)
        await asyncio.sleep(0)


asyncio.run(main())
