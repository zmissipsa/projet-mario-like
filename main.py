# main.py

import pygame
from player import Player
from level import Level
from sprites import Brick, Coin, Spritesheet
from enemy import Enemy, Spike


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

enemy_spritesheet = Spritesheet("./assets/images/characters.gif")
enemy1 = Enemy(400, 500, 400, 600, spritesheet=enemy_spritesheet)
enemy2 = Enemy(700, 500, 700, 900, spritesheet=enemy_spritesheet)
print(enemy1.image.get_size())  # Doit être (48, 48)
print(enemy1.rect.topleft)      # Vérifie la position sur l’écran

enemies = pygame.sprite.Group()
enemies.add(enemy1, enemy2)

# Créer des pics (pièges)
spikes = pygame.sprite.Group()
SPIKE_SIZE = 48
GROUND_Y = 500  # ou la hauteur réelle de la plateforme

spike1 = Spike(1050, GROUND_Y, spritesheet=enemy_spritesheet)
spike2 = Spike(200, GROUND_Y, spritesheet=enemy_spritesheet)
spikes.add(spike1, spike2)


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
    enemies.update()
    spikes.update()


    for brick in bricks:
     if brick.rect.colliderect(player.rect):  # ou une détection précise du saut
        coin = brick.break_brick()
        if coin:
            coins.add(coin)

 # Collisions avec les ennemis
    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy) and enemy.alive:
            if player.vel_y > 0 and player.rect.bottom <= enemy.rect.top + 10:
                enemy.kill_enemy()
                player.vel_y = -10  # rebond
            else:
                # Joueur meurt
                player.rect.topleft = (100, 100)

    # Collisions avec les pics
    # Collision mortelle avec un spike
    if pygame.sprite.spritecollide(player, spikes, False):
        font = pygame.font.SysFont("Arial", 72)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (400, 250))
        pygame.display.flip()
        pygame.time.wait(2000)  # Pause 2 secondes
        running = False  # Ferme le jeu

    # Affichage
    screen.fill((135, 206, 235))  # Bleu ciel

    level.draw(screen)                      # Dessin des plateforms
    screen.blit(player.image, player.rect)   # Dessin du joueur
    bricks.draw(screen)
    coins.draw(screen)
    enemies.draw(screen)
    spikes.draw(screen)
    
    pygame.display.flip()

    for platform in plateforms:
        if platform.type == "flag" and player.rect.colliderect(platform.rect):
            #passer au niveau 2
            level = Level("niveau2.txt", "tiles.xcf")
            player.rect.topleft = (100,100) #Réinitialise la position du joueur
            break

pygame.quit()
