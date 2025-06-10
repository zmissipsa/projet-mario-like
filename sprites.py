import pygame

class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), pygame.Rect(x, y, width, height))
        return image