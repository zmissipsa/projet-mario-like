# main.py

import pygame
from player import Player
from level import Level

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Mario-like")
clock = pygame.time.Clock()

level1 = Level("niveau1.txt", "tiles.xcf")

# Créer le player
player = Player(100, 100)
player_group = pygame.sprite.Group()
player_group.add(player)

running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player_group.update()


    # Affichage
    screen.fill((135, 206, 235))  # Bleu ciel

    level1.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

pygame.quit()
