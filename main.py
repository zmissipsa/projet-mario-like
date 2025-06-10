# main.py

import pygame
from player import Player
from level import Level

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Mario-like")
clock = pygame.time.Clock()

level = Level("niveau1.txt", "tiles.xcf")

# Créer le player
player = Player(100, 100)
#player_group = pygame.sprite.Group()
#player_group.add(player)

running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    plateforms = level.get_platforms()
    player.update(plateforms)


    # Affichage
    screen.fill((135, 206, 235))  # Bleu ciel

    level.draw(screen)                      # Dessin des plateforms
    screen.blit(player.image, player.rect)   # Dessin du joueur

    pygame.display.flip()

    for platform in plateforms:
        if platform.type == "flag" and player.rect.colliderect(platform.rect):
            #passer au niveau 2
            level = Level("niveau2.txt", "tiles.xcf")
            player.rect.topleft = (100,100) #Réinitialise la position du joueur
            break

pygame.quit()
