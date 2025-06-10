# main.py

import pygame
from player import Player
from level import Level
from sprites import Brick, Coin, Spritesheet


pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Mario-like")
clock = pygame.time.Clock()

level = Level("niveau1.txt", "tiles.xcf")

# Creer le player
player = Player(100, 100)
#player_group = pygame.sprite.Group()
#player_group.add(player)

spritesheet = Spritesheet("assets/images/tiles.xcf")

bricks = pygame.sprite.Group()
brick1 = Brick(300, 250, spritesheet, breakable=True)
brick2 = Brick(900, 350, spritesheet, breakable=True)
bricks.add(brick1, brick2)

coins = pygame.sprite.Group()

running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update

    plateforms = level.get_platforms()
    player.update(plateforms)

    bricks.update()
    coins.update()

    for brick in bricks:
     if brick.rect.colliderect(player.rect):  # ou une détection précise du saut
        coin = brick.break_brick()
        if coin:
            coins.add(coin)



    # Affichage
    screen.fill((135, 206, 235))  # Bleu ciel

    level.draw(screen)                      # Dessin des plateforms
    screen.blit(player.image, player.rect)   # Dessin du joueur
    bricks.draw(screen)
    coins.draw(screen)


    pygame.display.flip()

    for platform in plateforms:
        if platform.type == "flag" and player.rect.colliderect(platform.rect):
            #passer au niveau 2
            level = Level("niveau2.txt", "tiles.xcf")
            player.rect.topleft = (100,100) #Réinitialise la position du joueur
            break

pygame.quit()
