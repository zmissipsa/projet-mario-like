# player.py

import pygame
from sprites import Spritesheet

# 🔊 Initialiser le son de saut
try:
    pygame.mixer.init()
    jump_sound = pygame.mixer.Sound("assets/sounds/small_jump.ogg")
except Exception as e:
    jump_sound = None
    print("[WARNING] Le son de saut n'a pas pu être chargé :", e)



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Pour commencer, un simple carré rouge
        spritesheet = Spritesheet("./assets/images/characters.gif")
        
        #self.sprites ={
        #    "idle": pygame.transform.scale(spritesheet.get_image(256, 0, 20, 35), (48, 48)),
        #    "walk": pygame.transform.scale(spritesheet.get_image(256, 0, 20, 35), (48, 48)),
        #    "jump": pygame.transform.scale(spritesheet.get_image(368, 0, 20, 35), (48, 48)),
        #}
        self.walk_right = [
            pygame.transform.scale(spritesheet.get_image(296, 0, 16, 35), (48, 48)),
            pygame.transform.scale(spritesheet.get_image(314, 0, 16, 35), (48, 48))
        ]
        self.walk_left = [pygame.transform.flip(img, True, False) for img in self.walk_right]

        self.idle = pygame.transform.scale(spritesheet.get_image(256, 0, 20, 35), (48, 48))
        self.jump_right = pygame.transform.scale(spritesheet.get_image(368, 0, 20, 35), (48, 48))
        self.jump_left = pygame.transform.flip(self.jump_right, True, False)

        self.image = self.idle

        self.animation_counter = 0
        self.animation_speed = 10  # Frames entre chaque image de marche

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
        self.is_jumping_up = False

        # Préparation future pour les animations
        self.direction = "right"

        #ajout de vies pour le joueur
        self.lives = 3
        self.start_position = (x,y)

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
            if jump_sound:
                jump_sound.play()

    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > self.terminal_velocity:
            self.vel_y = self.terminal_velocity

    def update(self, platforms):
        self.handle_input()
        self.apply_gravity()

        # Mise à jour de is_jumping_up selon la vitesse verticale
        self.is_jumping_up = self.vel_y < 0

        # deplacement horizontal + collisions
        self.rect.x += self.vel_x
        self.check_collisions(platforms, "horizontal")

        #deplacement vertical + collisions
        self.rect.y += self.vel_y
        self.check_collisions(platforms, "vertical")

        #Choisir le sprite selon l'état
        if not self.on_ground:             #saut
            if self.direction == "right":
                self.image = self.jump_right
            else:
                self.image = self.jump_left
        elif self.vel_x!= 0:             #marche animée
            self.animation_counter += 1
            index = (self.animation_counter // self.animation_speed) % 2
            if self.direction == "right":
                self.image = self.walk_right[index]
            else:
                self.image = self.walk_left[index]
        else:
            self.image = self.idle
            self.animation_counter = 0 #reinitialisation de l'animation
        
        # Inverser l'image si vers la gauche
        #if self.direction == "left":
        #   self.image = pygame.transform.flip(self.image, True, False)

       
    
    def check_collisions(self, platforms, direction):
        for plateform in platforms:
            if hasattr(plateform, 'is_solid') and not plateform.is_solid:
                continue

            if self.rect.colliderect(plateform.rect):
                if direction == "horizontal":
                    if self.vel_x > 0:             #deplacement vers la droite
                        self.rect.right = plateform.rect.left
                    elif self.vel_x < 0: # gauche
                        self.rect.left = plateform.rect.right
                elif direction == "vertical":
                    if self.vel_y > 0 : #chute
                        self.rect.bottom = plateform.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0 : #saut
                        self.rect.top = plateform.rect.bottom
                        self.vel_y = 0
        if direction ==  "vertical" and self.vel_y != 0:
            self.on_ground = False
    
    def lose_life(self):
        self.lives -= 1
        self.rect.topleft = self.start_position
        self.vel_x = 0
        self.vel_y = 0