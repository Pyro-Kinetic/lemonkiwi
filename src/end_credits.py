import pygame
from support import sound_loader, music_loader, resource_path


class EndCredits:
    def __init__(self, surface, load_over_world):
        self.display = surface
        self.load_over_world = load_over_world

        # audio
        self.button_click_sound = sound_loader("../audio/button_click.mp3")
        self.button_click_sound.set_volume(0.5)

        self.troll_sound = sound_loader("../audio/loud_moaning.mp3")
        self.troll_sound.set_volume(10.0)

        # message
        self.message1 = "Congrats"
        self.message2 = "You completed level 5"
        self.message3 = "Click M to start new game"
        self.message4 = "Click T to for a surprise"
        self.message5 = "Thanks for playing!"
        self.font = pygame.font.Font(resource_path("../graphics/ui/ARCADEPI.ttf"), 50)

    def show_messages(self):
        text1 = self.font.render(self.message1, False, "skyblue1")
        text1_rect = text1.get_rect(center=(800, 200))

        text2 = self.font.render(self.message2, False, "skyblue1")
        text2_rect = text2.get_rect(center=(800, 300))

        text3 = self.font.render(self.message3, False, "skyblue1")
        text3_rect = text3.get_rect(center=(800, 400))

        text4 = self.font.render(self.message4, False, "skyblue1")
        text4_rect = text4.get_rect(center=(800, 500))

        text5 = self.font.render(self.message5, False, "skyblue1")
        text5_rect = text5.get_rect(center=(800, 600))

        self.display.blit(text1, text1_rect)
        self.display.blit(text2, text2_rect)
        self.display.blit(text3, text3_rect)
        self.display.blit(text4, text4_rect)
        self.display.blit(text5, text5_rect)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            pygame.mixer.music.stop()
            music_loader("../audio/upbeat_pop.wav")
            self.button_click_sound.play()
            self.load_over_world()
        if keys[pygame.K_t]:
            pygame.mixer.music.stop()
            self.troll_sound.play(-1)

    def run(self):
        self.display.fill("black")
        self.show_messages()
        self.input()
