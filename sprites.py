import pygame

class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), pygame.Rect(x, y, width, height))
        return image
        
import pygame

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, breakable=True, content="coin", is_pipe=False):
        super().__init__()
        self.sheet = sheet
        # On extrait l’image de la brique (16x16 px à la position 384,63 dans la spritesheet)
        self.image = sheet.get_image(384, 63, 16, 16)
        # On agrandit l’image à 32x32 px pour le rendu
        self.image = pygame.transform.scale(self.image, (32, 32))
        # Positionne la brique dans la fenêtre avec son coin supérieur gauche à (x,y)
        self.rect = self.image.get_rect(topleft=(x, y))
        # Attribut qui dit si la brique est cassable ou pas
        self.breakable = breakable
        # Attribut indiquant si la brique a été frappée (au début non)
        self.hit = False
        # Contenu caché dans la brique, par exemple "coin", "star", ou None
        self.content = content
        # Nouveau booléen indiquant si cette brique est un tuyau vert
        self.is_pipe = is_pipe

    def break_brick(self):
        # Si la brique est incassable, on ne fait rien
        if not self.breakable:
            return None
        # Sinon on détruit la brique
        self.kill()
        # On crée et retourne l’objet contenu, si il y en a un
        if self.content == "coin":
            return Coin(self.rect.centerx, self.rect.top - 10, self.sheet)
        elif self.content == "star":
            return Star(self.rect.centerx, self.rect.top - 10, self.sheet)
        # Pas de contenu, retourne None par défaut
        return None



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
