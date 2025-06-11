import pygame
from sprites import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        spritesheet = Spritesheet("./assets/images/characters.gif")
        
        self.sprites = {
            "idle": pygame.transform.scale(spritesheet.get_image(256, 0, 20, 35), (48, 48)),
            "walk": pygame.transform.scale(spritesheet.get_image(256, 0, 20, 35), (48, 48)),
            "jump": pygame.transform.scale(spritesheet.get_image(368, 0, 20, 35), (48, 48)),
        }
        
        self.image = self.sprites["idle"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_strength = 15
        self.gravity = 0.8
        self.terminal_velocity = 12

        self.on_ground = False
        self.is_jumping_up = False  # <-- Ajout ici

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

    def update(self, platforms):
        self.handle_input()
        self.apply_gravity()

        # Mise à jour de is_jumping_up selon la vitesse verticale
        self.is_jumping_up = self.vel_y < 0

        # déplacement horizontal + collisions
        self.rect.x += self.vel_x
        self.check_collisions(platforms, "horizontal")

        # déplacement vertical + collisions
        self.rect.y += self.vel_y
        self.check_collisions(platforms, "vertical")

        # Choisir le sprite selon l'état
        if not self.on_ground:
            self.image = self.sprites["jump"]
        elif self.vel_x != 0:
            self.image = self.sprites["walk"]
        else:
            self.image = self.sprites["idle"]

        # Inverser l'image si vers la gauche
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def check_collisions(self, platforms, direction):
        for plateform in platforms:
            if hasattr(plateform, 'is_solid') and not plateform.is_solid:
                continue

            if self.rect.colliderect(plateform.rect):
                if direction == "horizontal":
                    if self.vel_x > 0:
                        self.rect.right = plateform.rect.left
                    elif self.vel_x < 0:
                        self.rect.left = plateform.rect.right
                elif direction == "vertical":
                    if self.vel_y > 0:
                        self.rect.bottom = plateform.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:
                        self.rect.top = plateform.rect.bottom
                        self.vel_y = 0

        if direction == "vertical" and self.vel_y != 0:
            self.on_ground = False
