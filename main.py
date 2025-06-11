import pygame
from player import Player
from level import Level
import sprites

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Mario-like")
clock = pygame.time.Clock()

#Liste des niveaux
level_files = ["niveau1.txt","niveau2.txt","niveau3.txt"]
current_level_index = 0

# Font pour le score
font = pygame.font.SysFont(None, 36)

#charger le premier niveau
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

bricks.add(brick3, brick4)


bricks.add(brick1, brick2)

coins = pygame.sprite.Group()

# Créer le player
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
    
    for platform in plateforms:
        if platform.type == "flag" and player.rect.colliderect(platform.rect):
            current_level_index += 1
            if current_level_index >= len(level_files):
                print("Jeu terminé")
                running = False
                break
            else:
                level = Level(level_files[current_level_index], "tiles.xcf")
                player.rect.topleft = (100,100) #Réinitialise la position du joueur
                break
    
    # Affichage
    screen.fill((135, 206, 235))  # Bleu ciel

    level.draw(screen)                      # Dessin des plateforms
    screen.blit(player.image, player.rect)   # Dessin du joueur
    bricks.draw(screen)
    coins.draw(screen)

    # Affichage texte
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    coins_text = font.render(f"Pièces: {coins_collected}", True, (255, 215, 0))
    stars_text = font.render(f"Étoiles: {stars_collected}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (10, 40))
    screen.blit(stars_text, (10, 70))

    pygame.display.flip()

pygame.quit()
