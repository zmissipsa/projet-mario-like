import pygame
from player import Player
from level import Level
import sprites

# Puis dans ton code utilise sprites.Star, sprites.Brick, etc.


# Initialisation
pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Mario-like")
clock = pygame.time.Clock()

# Font pour le score
font = pygame.font.SysFont(None, 36)

# Chargement des ressources
spritesheet = sprites.Spritesheet("assets/images/tiles.xcf")


# Niveau
level = Level("niveau1.txt", "tiles.xcf")
plateforms = level.get_platforms()

# Joueur
player = Player(100, 100)

# Groupes
bricks = pygame.sprite.Group()
collectibles = pygame.sprite.Group()  # contiendra pièces et étoiles

# Création de briques : coin ou star
brick1 = sprites.Brick(300, 250, spritesheet, breakable=True, content="coin")
brick2 = sprites.Brick(900, 350, spritesheet, breakable=True, content="star")
brick3 = sprites.Brick(500, 250, spritesheet, breakable=True, content="coin")
brick4 = sprites.Brick(700, 300, spritesheet, breakable=True, content="star")

bricks.add(brick3, brick4)


bricks.add(brick1, brick2)

# Score
score = 0
coins_collected = 0
stars_collected = 0

# Boucle principale
running = True
while running:
    clock.tick(60)

    # Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    plateforms = level.get_platforms()
    player.update(plateforms)
    bricks.update()
    collectibles.update()

    # Collision avec les briques
    for brick in bricks:
     if player.rect.colliderect(brick.rect) and player.is_jumping_up:
        item = brick.break_brick()
        if item:
            collectibles.add(item)
            if isinstance(item, sprites.Coin):
                score += 10
                coins_collected += 1
            elif isinstance(item, sprites.Star):
                score += 50
                stars_collected += 1


    # Affichage
    screen.fill((135, 206, 235))  # Bleu ciel
    level.draw(screen)
    screen.blit(player.image, player.rect)
    bricks.draw(screen)
    collectibles.draw(screen)

    # Affichage texte
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    coins_text = font.render(f"Pièces: {coins_collected}", True, (255, 215, 0))
    stars_text = font.render(f"Étoiles: {stars_collected}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (10, 40))
    screen.blit(stars_text, (10, 70))

    pygame.display.flip()

    # Passage au niveau suivant
    for platform in plateforms:
        if platform.type == "flag" and player.rect.colliderect(platform.rect):
            level = Level("niveau2.txt", "tiles.xcf")
            player.rect.topleft = (100, 100)
            break

pygame.quit()


