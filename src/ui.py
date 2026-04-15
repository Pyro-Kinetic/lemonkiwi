import pygame
from support import image_loader, resource_path


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        # fruits
        self.fruit = image_loader("../graphics/ui/bananas_idle.png")
        self.fruit_rect = self.fruit.get_rect(topleft=(700, 10))
        self.font = pygame.font.Font(resource_path("../graphics/ui/ARCADEPI.ttf"), 30)

    def show_fruits(self, amount):
        fruit_amount_text = self.font.render(str(amount), False, "#ffffff")
        fruit_amount_text_position = fruit_amount_text.get_rect(
            midleft=(self.fruit_rect.right + 5, self.fruit_rect.centery))

        self.display_surface.blit(self.fruit, self.fruit_rect)
        self.display_surface.blit(fruit_amount_text, fruit_amount_text_position)
