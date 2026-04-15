import pygame
from support import image_loader, sound_loader, resource_path


class OverWorld:
    def __init__(self, surface, load_level):
        self.title_name_rect = None
        self.display_surface = surface
        self.load_level = load_level

        # audio
        self.button_click_sound = sound_loader("../audio/button_click.mp3")
        self.button_click_sound.set_volume(0.5)

        # player
        self.player = image_loader("../graphics/main_characters/test.png")
        self.player_rect = self.player.get_rect(center=(800, 400))

        # font
        self.font = pygame.font.Font(resource_path("../graphics/ui/ARCADEPI.ttf"), 50)
        self.lemon_text = "LEMON"
        self.kiwi_text = "KIWI"
        self.prompt_text = "Press space to start"

    def show_lemon(self, text):
        title_name = self.font.render(text, False, "yellow")
        self.title_name_rect = title_name.get_rect(center=(730, self.player_rect.top - 80))

        self.display_surface.blit(title_name, self.title_name_rect)

    def show_kiwi(self, text):
        title_name = self.font.render(text, False, "yellowgreen")
        title_name_rect = title_name.get_rect(center=(920, self.player_rect.top - 80))

        self.display_surface.blit(title_name, title_name_rect)

    def show_prompt(self, text):
        prompt = self.font.render(text, False, "skyblue1")
        prompt_rect = prompt.get_rect(center=(800, self.player_rect.bottom + 150))

        self.display_surface.blit(prompt, prompt_rect)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.button_click_sound.play()
            self.load_level()

    def run(self):
        self.input()
        self.display_surface.fill("black")
        self.show_lemon(self.lemon_text)
        self.show_kiwi(self.kiwi_text)
        self.show_prompt(self.prompt_text)
        self.display_surface.blit(self.player, self.player_rect)
