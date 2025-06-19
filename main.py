import pygame
from player import Player
from level import Level
from sprites import Brick, Coin, Star, Spritesheet
from enemy import Enemy, Spike
import sprites

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Mario-like")
clock = pygame.time.Clock()

# Liste des fichiers de niveaux
level_files = ["niveau1.txt", "niveau2.txt", "niveau3.txt"]
current_level_index = 0

GROUND_Y = 500

font = pygame.font.SysFont(None, 36)

enemy_spritesheet = sprites.Spritesheet("./assets/images/characters.gif")
tiles_spritesheet = sprites.Spritesheet("assets/images/tiles.xcf")

def load_level(level_index):
    level = Level(level_files[level_index], "tiles.xcf")

    # Groupes vides
    bricks = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    # Selon le niveau, créer briques, ennemis, spikes
    if level_index == 0:
        bricks.add(
            sprites.Brick(300, 250, tiles_spritesheet, breakable=True, content="coin"),
            sprites.Brick(900, 350, tiles_spritesheet, breakable=True, content="star"),
            sprites.Brick(500, 250, tiles_spritesheet, breakable=True, content="coin"),
            sprites.Brick(700, 300, tiles_spritesheet, breakable=True, content="star"),
        )
        enemies.add(
            Enemy(400, 500, 400, 600, spritesheet=enemy_spritesheet),
            Enemy(700, 500, 700, 900, spritesheet=enemy_spritesheet),
        )
        spikes.add(
            Spike(1050, GROUND_Y, spritesheet=enemy_spritesheet),
            Spike(200, GROUND_Y, spritesheet=enemy_spritesheet),
        )
    elif level_index == 1:
        # Exemple niveau 2 : modifier coordonnées selon besoin
        bricks.add(
            sprites.Brick(350, 300, tiles_spritesheet, breakable=True, content="coin"),
            sprites.Brick(800, 280, tiles_spritesheet, breakable=True, content="star"),
        )
        enemies.add(
            Enemy(500, 500, 450, 650, spritesheet=enemy_spritesheet),
        )
        spikes.add(
            Spike(1000, GROUND_Y, spritesheet=enemy_spritesheet),
        )
    elif level_index == 2:
        # Exemple niveau 3 : modifier coordonnées selon besoin
        bricks.add(
            sprites.Brick(400, 260, tiles_spritesheet, breakable=True, content="coin"),
            sprites.Brick(850, 330, tiles_spritesheet, breakable=True, content="star"),
        )
        enemies.add(
            Enemy(600, 500, 550, 750, spritesheet=enemy_spritesheet),
            Enemy(900, 500, 850, 1050, spritesheet=enemy_spritesheet),
        )
        spikes.add(
            Spike(1100, GROUND_Y, spritesheet=enemy_spritesheet),
        )

    return level, bricks, enemies, spikes, collectibles

# Charger premier niveau
level, bricks, enemies, spikes, collectibles = load_level(current_level_index)

player = Player(100, 100)

score = 0
coins_collected = 0
stars_collected = 0

running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    plateforms = level.get_platforms()

    player.update(plateforms)
    bricks.update()
    collectibles.update()
    enemies.update()
    spikes.update()

    # Collision avec briques
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

    # Collision avec ennemis
    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy) and enemy.alive:
            if player.vel_y > 0 and player.rect.bottom <= enemy.rect.top + 10:
                enemy.kill_enemy()
                player.vel_y = -10  # rebond
            else:
                player.rect.topleft = (100, 100)

    # Collision avec pics
    if pygame.sprite.spritecollide(player, spikes, False):
        font_game_over = pygame.font.SysFont("Arial", 72)
        game_over_text = font_game_over.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (400, 250))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Passage niveau
    for platform in plateforms:
        if platform.type == "flag" and player.rect.colliderect(platform.rect):
            current_level_index += 1
            if current_level_index >= len(level_files):
                print("Jeu terminé")
                running = False
                break
            else:
                level, bricks, enemies, spikes, collectibles = load_level(current_level_index)
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

    # Texte score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    coins_text = font.render(f"Pièces: {coins_collected}", True, (255, 215, 0))
    stars_text = font.render(f"Étoiles: {stars_collected}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (10, 40))
    screen.blit(stars_text, (10, 70))

    pygame.display.flip()

pygame.quit()

