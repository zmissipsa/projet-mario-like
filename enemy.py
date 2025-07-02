# enemy.py

import pygame
import random
from sprites import Spritesheet
import math
# Ennemi mobile
class Enemy(pygame.sprite.Sprite):
    """
    Classe Enemy : - Gère un ennemi mobile se déplaçant horizontalement.
    - Se déplace entre deux bornes définies dans le niveau.
    - Inverse sa direction lorsqu'il atteint une borne.
    - Méthodes principales :
        update() : met à jour la position et l'image selon la direction.
        crush() : désactive l'ennemi lorsque le joueur saute dessus.
    """
    def __init__(self, x, y, left_bound, right_bound, spritesheet, speed=2):
        super().__init__()
        
        # Image originale (direction droite)
        original_image = pygame.transform.scale(
            spritesheet.get_image(314, 206, 18, 25), (45, 45)
        )
        # Image retournée horizontalement (direction gauche)
        self.image_right = original_image
        self.image_left = pygame.transform.flip(original_image, True, False)

        self.crushed_img = pygame.transform.scale(
            spritesheet.get_image(334, 215, 16, 15),(32, 25)  # écrasé plus petit en hauteur
        )
        
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
            if self.timer and pygame.time.get_ticks() - self.timer > 500:
                self.kill()
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

    def crush(self):
        # Appelé quand Mario saute dessus
        if self.alive:
            self.image = self.crushed_img
            # Ajuste le rect car l'image est plus petite
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.alive = False
            self.timer = pygame.time.get_ticks()

# Obstacle fixe
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet):
        super().__init__()
        
        # Extraire le sprite des pics depuis le spritesheet général
        self.image = pygame.transform.scale(
            spritesheet.get_image(126, 180, 16, 23), (45, 45) 
        )
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class PiranhaPlant(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet):
        super().__init__()
        self.sheet = spritesheet

        self.closed_img = pygame.transform.scale(
            spritesheet.get_image(351, 174, 18, 33),
            (36, 66)
        )
        self.open_img = pygame.transform.scale(
            spritesheet.get_image(333, 181, 18, 22),(50, 58)
        )

        self.image = self.closed_img

        y_closed = y + 55
        self.rect = self.image.get_rect(bottomleft=(x, y_closed))

        self.base_y = y_closed
        self.up_y = y_closed - 65

        self.speed = 1

        self.state = "hidden"
        self.timer = pygame.time.get_ticks()

        self.image.set_alpha(0)  # invisible au départ

    def update(self):
        now = pygame.time.get_ticks()

        if self.state == "hidden":
            self.image.set_alpha(0)  # invisible dans le tuyau
            if now - self.timer > 2000:
                self.state = "rising"
                self.timer = now
                self.image = self.closed_img
                self.image.set_alpha(255)  # visible mais fermée dès qu'elle commence à monter

        elif self.state == "rising":
            self.rect.y -= self.speed
            # plante visible fermée tant qu'elle n'est pas sortie
            self.image = self.closed_img
            self.image.set_alpha(255)
            if self.rect.y <= self.up_y:
                self.rect.y = self.up_y
                self.state = "open"
                self.timer = now
                self.image = self.open_img
                self.image.set_alpha(255)

        elif self.state == "open":
            self.image = self.open_img
            self.image.set_alpha(255)
            if now - self.timer > 2000:
                self.state = "falling"
                self.timer = now
                self.image = self.closed_img  # refermer avant de descendre

        elif self.state == "falling":
            self.rect.y += self.speed
            self.image = self.closed_img
            self.image.set_alpha(255)
            if self.rect.y >= self.base_y:
                self.rect.y = self.base_y
                self.state = "hidden"
                self.timer = now
                self.image.set_alpha(0)  # invisible dans le tuyau

    def draw(self, surface):
        if self.state != "hidden":
            surface.blit(self.image, self.rect)




class BlueGoomba(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet, min_x, max_x):
        super().__init__()
        self.sheet = spritesheet

        # Récupère les images
        self.normal_img = pygame.transform.scale(
            spritesheet.get_image(238,185,18, 22),
            (45, 45)  # ou une autre taille selon ton jeu
        )
        self.crushed_img = pygame.transform.scale(
            spritesheet.get_image(220, 187, 16, 21),
            (32, 16)  # écrasé plus petit en hauteur
        )

        self.image = self.normal_img
        self.rect = self.image.get_rect(topleft=(x, y))

        # Mouvements
        self.speed = 2
        self.direction = 1  # commence vers la droite
        self.min_x = min_x
        self.max_x = max_x
        self.alive = True
        self.timer = None
        

    def update(self):
        if self.alive:
            # Déplacement va-et-vient
            self.rect.x += self.speed * self.direction

            # Inverse la direction si on dépasse les bornes
            if self.rect.x < self.min_x:
                self.rect.x = self.min_x
                self.direction = 1
            elif self.rect.x > self.max_x:
                self.rect.x = self.max_x
                self.direction = -1
        else:
            if self.timer and pygame.time.get_ticks() - self.timer > 500:
                self.kill()

    def crush(self):
        # Appelé quand Mario saute dessus
        if self.alive:
            self.image = self.crushed_img
            # Ajuste le rect car l'image est plus petite
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.alive = False
            self.timer = pygame.time.get_ticks()
            
class FlyingGhost(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet, enemy_group, all_sprites):
        super().__init__()
        self.sheet = spritesheet  
        self.direction = 1
        self.speed = 1
        self.left_bound = 1400
        self.right_bound = 2300
        self.base_y = y - 50  # ← fantôme 50px plus haut
        self.angle = 0
        self.alive = True
        self.timer = None

        # Apparence du fantôme
        self.image_right = pygame.transform.scale(
            self.sheet.get_image(238, 259, 19, 26),
            (45, 45)
        )
        self.image = self.image_right
        self.rect = self.image.get_rect(midbottom=(x, self.base_y))

        # Groupes
        self.enemy_group = enemy_group
        self.all_sprites = all_sprites
        self.last_attack_time = pygame.time.get_ticks() + random.randint(0, 2000)

    def update(self):
        if not self.alive:
            if self.timer and pygame.time.get_ticks() - self.timer > 500:
                self.kill()
            return

        # Déplacement horizontal
        self.rect.x += self.direction * self.speed
        if self.rect.left <= self.left_bound:
            self.rect.left = self.left_bound
            self.direction = 1
        elif self.rect.right >= self.right_bound:
            self.rect.right = self.right_bound
            self.direction = -1

        # Apparence selon direction
        if self.direction == 1:
            self.image = self.image_right
        else:
            self.image = pygame.transform.flip(self.image_right, True, False)

        # Flottement vertical
        self.angle += 0.05
        offset_y = math.sin(self.angle) * 5
        self.rect.y = self.base_y + offset_y

        # Spawn ennemi toutes les 15 secondes
        now = pygame.time.get_ticks()
        if now - self.last_attack_time >= 15000:
            self.spawn_enemy()
            self.last_attack_time = now

    def spawn_enemy(self):
        falling_enemy = FallingEnemy(self.rect.centerx, self.rect.bottom - 30, self.sheet)
        self.enemy_group.add(falling_enemy)
        self.all_sprites.add(falling_enemy)

    def crush(self):
        if self.alive:
            self.image = pygame.transform.scale(
                self.sheet.get_image(257, 260, 19, 19),
                (32, 32)
            )
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.alive = False
            self.timer = pygame.time.get_ticks()
            
class FallingEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet):
        super().__init__()
        self.sheet = spritesheet

        self.image_right = pygame.transform.scale(
            self.sheet.get_image(293, 315, 19, 18), (45, 45)
        )
        self.image_left = pygame.transform.scale(
            self.sheet.get_image(180, 313, 18, 19), (45, 45)
        )
        self.image = self.image_left

        self.rect = self.image.get_rect(center=(x, y))

        self.vel_y = 5
        self.vel_x = 2
        self.spawn_time = pygame.time.get_ticks()
        self.on_ground = False
        self.alive = True
        self.timer = None

    def update(self, platforms):
        if self.alive:
            # Gravité
            if not self.on_ground:
                self.rect.y += self.vel_y
                for plat in platforms:
                    if self.rect.colliderect(plat.rect) and abs(self.rect.bottom - plat.rect.top) <= 10:
                        self.rect.bottom = plat.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                        break
            else:
                # Mouvement horizontal
                self.rect.x += self.vel_x

                # Bords de la zone
                if self.rect.left <= 1400 or self.rect.right >= 2300:
                    self.vel_x *= -1

                # Sol en dessous
                under_feet = self.rect.move(self.vel_x, 2)
                if not any(under_feet.colliderect(p.rect) for p in platforms):
                    self.vel_x *= -1

                # Animation direction
                if self.vel_x > 0:
                    self.image = self.image_right
                else:
                    self.image = self.image_left

        else:
            if self.timer and pygame.time.get_ticks() - self.timer > 500:
                self.kill()

    def crush(self):
        if self.alive:
            self.image = pygame.transform.scale(
                self.sheet.get_image(217, 313, 21, 17),
                (32, 26)
            )
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.alive = False
            self.timer = pygame.time.get_ticks()

