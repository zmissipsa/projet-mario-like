import pygame
from player import Player
from level import Level
from sprites import Brick, Coin, Spritesheet
from enemy import Enemy, Spike
import sprites

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Mario-like")
clock = pygame.time.Clock()

# Liste des niveaux
level_files = ["niveau1.txt", "niveau2.txt", "niveau3.txt"]
current_level_index = 0

# Font pour le score
font = pygame.font.SysFont(None, 36)

# Charger le premier niveau
level = Level(level_files[current_level_index], "tiles.xcf")
spritesheet = sprites.Spritesheet("assets/images/tiles.xcf")

# Groupes
bricks = pygame.sprite.Group()
collectibles = pygame.sprite.Group()  # contiendra pièces et étoiles

# Création de briques : coin ou star
brick1 = sprites.Brick(300, 250, spritesheet, breakable=True, content="coin")
brick2 = sprites.Brick(900, 350, spritesheet, breakable=True, content="star")
brick3 = sprites.Brick(500, 250, spritesheet, breakable=True, content="coin")
brick4 = sprites.Brick(700, 300, spritesheet, breakable=True, content="star")
bricks.add(brick1, brick2, brick3, brick4)

# Ennemis
enemy_spritesheet = Spritesheet("./assets/images/characters.gif")
enemy1 = Enemy(400, 500, 400, 600, spritesheet=enemy_spritesheet)
enemy2 = Enemy(700, 500, 700, 900, spritesheet=enemy_spritesheet)
enemies = pygame.sprite.Group()
enemies.add(enemy1, enemy2)

# Pics
spikes = pygame.sprite.Group()
GROUND_Y = 500
spike1 = Spike(1050, GROUND_Y, spritesheet=enemy_spritesheet)
spike2 = Spike(200, GROUND_Y, spritesheet=enemy_spritesheet)
spikes.add(spike1, spike2)

# Joueur
player = Player(100, 100)

# Score
score = 0
coins_collected = 0
stars_collected = 0

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
    collectibles.update()
    enemies.update()
    spikes.update()

    # Collision avec les briques et score
    for brick in bricks:
        if brick.rect.colliderect(player.rect) and player.is_jumping_up:
            item = brick.break_brick()
            if item:
                collectibles.add(item)
                if isinstance(item, sprites.Coin):
                    score += 10
                    coins_collected += 1
                elif isinstance(item, sprites.Star):
                    score += 50
                    stars_collected += 1

    # Collisions avec les ennemis
    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy) and enemy.alive:
            if player.vel_y > 0 and player.rect.bottom <= enemy.rect.top + 10:
                enemy.kill_enemy()
                player.vel_y = -10  # rebond
            else:
                player.rect.topleft = (100, 100)

    # Collisions avec les pics
    if pygame.sprite.spritecollide(player, spikes, False):
        font = pygame.font.SysFont("Arial", 72)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (400, 250))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Passage de niveau
    for platform in plateforms:
        if platform.type == "flag" and player.rect.colliderect(platform.rect):
            current_level_index += 1
            if current_level_index >= len(level_files):
                print("Jeu terminé")
                running = False
                break
            else:
                level = Level(level_files[current_level_index], "tiles.xcf")
                player.rect.topleft = (100, 100)
                break

    # Affichage
    screen.fill((135, 206, 235))  # Bleu ciel
    level.draw(screen)
    screen.blit(player.image, player.rect)
    bricks.draw(screen)
    collectibles.draw(screen)
    enemies.draw(screen)
    spikes.draw(screen)

    # Affichage texte
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    coins_text = font.render(f"Pièces: {coins_collected}", True, (255, 215, 0))
    stars_text = font.render(f"Étoiles: {stars_collected}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (10, 40))
    screen.blit(stars_text, (10, 70))

    pygame.display.flip()

pygame.quit()
