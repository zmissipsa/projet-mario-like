# player.py

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Pour commencer, un simple carré rouge
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Mouvements
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_strength = 15
        self.gravity = 0.8
        self.terminal_velocity = 12

        self.on_ground = False

        # Préparation future pour les animations
        self.direction = "right"

    def handle_input(self):
        keys = pygame.key.get_pressed()

        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.direction = "right"

        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > self.terminal_velocity:
            self.vel_y = self.terminal_velocity

    def update(self):
        self.handle_input()
        self.apply_gravity()

        # Mise à jour de la position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # TEMP : collision avec le sol
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Limiter le déplacement à l'écran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:  # largeur de l'écran
            self.rect.right = 800
