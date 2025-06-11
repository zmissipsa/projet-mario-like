import pygame

class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), pygame.Rect(x, y, width, height))
        return image
        
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, breakable=True, content="coin"):
        super().__init__()
        self.sheet = sheet
        self.image = sheet.get_image(384, 63, 16, 16)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.breakable = breakable
        self.hit = False
        self.content = content  # "coin" ou "star"

    def break_brick(self):
        if not self.breakable:
            return None

        self.kill()

        if self.content == "coin":
            return Coin(self.rect.centerx, self.rect.top - 10, self.sheet)
        elif self.content == "star":
            return Star(self.rect.centerx, self.rect.top - 10, self.sheet)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet):
        super().__init__()
        # *** ICI on extrait 16×16 à (385, 81) depuis le même sheet ***
        self.image = sheet.get_image(385, 81, 15, 15)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect  = self.image.get_rect(center=(x, y))
        self.timer = 30                            # durée d’affichage

    def update(self):
        self.rect.y -= 1      # monte doucement
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            
class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet):
        super().__init__()
        self.image = sheet.get_image(241, 81, 15, 15)  # adapte selon ta sprite sheet
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 30

    def update(self):
        self.rect.y -= 1
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
