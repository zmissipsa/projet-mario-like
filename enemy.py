# enemy.py

import pygame
from sprites import Spritesheet

# Ennemi mobile
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, left_bound, right_bound, spritesheet, speed=2):
        super().__init__()
        
        # Image originale (direction droite)
        original_image = pygame.transform.scale(
            spritesheet.get_image(256, 368, 20, 35), (48, 48)
        )
        # Image retournée horizontalement (direction gauche)
        self.image_right = original_image
        self.image_left = pygame.transform.flip(original_image, True, False)
        
        # Par défaut, regarde vers la droite
        self.image = self.image_right
        
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = speed
        self.direction = 1  # 1 = droite, -1 = gauche
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.rect.x += self.speed * self.direction

        # Inverser la direction si les limites sont atteintes
        if self.rect.left <= self.left_bound:
            self.direction = 1
        elif self.rect.right >= self.right_bound:
            self.direction = -1

        # Mettre à jour l’image selon la direction
        if self.direction == 1:
            self.image = self.image_right
        else:
            self.image = self.image_left

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)

    def kill_enemy(self):
        self.alive = False

# Obstacle fixe
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet):
        super().__init__()
        
        # Extraire le sprite des pics depuis le spritesheet général
        self.image = pygame.transform.scale(
            spritesheet.get_image(124, 170, 20, 35), (48, 48)  # Coordonnées à ajuster selon l'image
        )
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    # À ajouter à la fin de enemy.py
class PiranhaPlant(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet):
        super().__init__()
        self.sheet = spritesheet

        # Agrandir images (2x taille)
        self.closed_img = pygame.transform.scale(
            spritesheet.get_image(351, 174, 18, 33),
            (36, 66)
        )
        self.open_img = pygame.transform.scale(
            spritesheet.get_image(330, 179, 25, 29),
            (50, 58)
        )

        self.image = self.closed_img
        
        # Position fermée plus basse (plus enfoncée dans le tuyau)
        y_closed = y + 55
        self.rect = self.image.get_rect(bottomleft=(x, y_closed))

        self.base_y = y_closed
        self.up_y = y_closed - 65  # hauteur sortie un peu plus haute

        self.speed = 1

        self.state = "hidden"
        self.timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()

        if self.state == "hidden":
            if now - self.timer > 2000:
                self.state = "rising"
                self.timer = now

        elif self.state == "rising":
            self.rect.y -= self.speed
            if self.rect.y <= self.up_y:
                self.rect.y = self.up_y
                self.state = "open"
                self.timer = now
                self.image = self.open_img

        elif self.state == "open":
            if now - self.timer > 2000:
                self.state = "falling"
                self.timer = now
                self.image = self.closed_img

        elif self.state == "falling":
            self.rect.y += self.speed
            if self.rect.y >= self.base_y:
                self.rect.y = self.base_y
                self.state = "hidden"
                self.timer = now

