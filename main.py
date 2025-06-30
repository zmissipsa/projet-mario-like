import pygame
from player import Player
from level import Level
from sprites import Brick, Coin, Star, Spritesheet
from enemy import Enemy, Spike, PiranhaPlant, BlueGoomba
from menu import menu
# Constantes
SCREEN_W, SCREEN_H = 1200, 600
GROUND_Y = 500

COUNTDOWN_MS = 3000 # 10 secondes avant démarrage du jeu

# Initialisation Pygame et fenêtre
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Mario-like")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
menu(screen)

# Chargement des spritesheets
tiles_sheet = Spritesheet("assets/images/tiles.png")
enemy_sheet = Spritesheet("assets/images/characters.gif")

def build_world_for_level(level_idx):
    bricks, enemies, spikes = (pygame.sprite.Group() for _ in range(3))
    plantes_group = pygame.sprite.Group()  # Groupe plantes Piranha

    if level_idx == 0:
        bricks.add(
            Brick(300, 250, tiles_sheet, True, "coin"),
            Brick(500, 250, tiles_sheet, True, "coin"),
            Brick(700, 300, tiles_sheet, True, "star"),
            Brick(900, 350, tiles_sheet, True, "star"),
        )
        enemies.add(
            Enemy(400, GROUND_Y, 400, 600, enemy_sheet),
            Enemy(700, GROUND_Y, 650, 1100, enemy_sheet),
        )
        spikes.add(
            Spike(1050, GROUND_Y, enemy_sheet),
            Spike(200, GROUND_Y, enemy_sheet),
        )

    elif level_idx == 1:
        bricks.add(
            Brick(300, 250, tiles_sheet, True, "coin"),
            Brick(500, 250, tiles_sheet, True, "star"),
            Brick(700, 250, tiles_sheet, True, "coin"),
            Brick(1100, 250, tiles_sheet, True, "star"),
            Brick(1400, 350, tiles_sheet, True, "star"),
            Brick(1800, 150, tiles_sheet, True, "coin"),
            Brick(2000, 200, tiles_sheet, True, "coin")
        )

        enemies.add(
            Enemy(2000, GROUND_Y, 400, 700, enemy_sheet),
            Enemy(1500, GROUND_Y, 700, 1000, enemy_sheet),
            Enemy(1100, GROUND_Y, 1000, 1250, enemy_sheet),
            Enemy(1800, GROUND_Y, 1300, 1500, enemy_sheet),
            BlueGoomba(1300, GROUND_Y - 35, enemy_sheet, 1000, 1400)

        )

        spikes.add(
            Spike(400, GROUND_Y, enemy_sheet),
            Spike(250, GROUND_Y, enemy_sheet),
            Spike(600, GROUND_Y, enemy_sheet),
            Spike(800, GROUND_Y, enemy_sheet),
            Spike(1000, GROUND_Y, enemy_sheet),
            Spike(1200, GROUND_Y, enemy_sheet),
        )

        # Liste des coordonnées des tuyaux (x, y)
        tuyaux = [
            (1500, 450),  # tuyau 1
            (1600, 400),  # tuyau 2
            (1700, 350),  # tuyau 3
            (1800, 300),  # tuyau 4
            (1900, 350),  # tuyau 5
            (2000, 400),  # tuyau 6
            (2100, 450)   # tuyau 7
        ]

        # Indices des tuyaux où mettre la plante (1, 4, 6, 7)
        tuyaux_plantes_indices = [0, 3, 5, 6]

        plante_height = 38  # Ajusté pour la taille correcte

        for i in tuyaux_plantes_indices:
            x, y = tuyaux[i]
            plante = PiranhaPlant(x + 25, y - plante_height, enemy_sheet)  # +25 pour centrage horizontal
            plantes_group.add(plante)

    return bricks, enemies, spikes, plantes_group


def find_spawn(level, x_world):
    """Trouve la meilleure position y pour faire apparaître le joueur à la coordonnée x."""
    best_top = SCREEN_H
    for p in level.get_platforms():
        if p.is_solid and p.rect.left <= x_world <= p.rect.right:
            best_top = min(best_top, p.rect.top)
    if best_top == SCREEN_H:
        best_top = GROUND_Y - 50
    return best_top - 48

def countdown_left(start_ms):
    """Retourne le temps (en ms) restant avant que le jeu commence, 0 si terminé."""
    return max(0, COUNTDOWN_MS - (pygame.time.get_ticks() - start_ms))

def show_game_over():
    text = pygame.font.SysFont("Arial", 72).render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, text.get_rect(center=(SCREEN_W//2, SCREEN_H//2)))
    pygame.display.flip()
    pygame.time.wait(2000)

# Chargement des niveaux
level_files = ["niveau1.txt", "niveau2.txt"]
current_level_id = 0

# Initialisation du niveau
level = Level(level_files[current_level_id], "tiles.png")
bricks, enemies, spikes, plantes_group = build_world_for_level(current_level_id)
collectibles = pygame.sprite.Group()

spawn_x = 100
player = Player(spawn_x, find_spawn(level, spawn_x))

game_start_ms = pygame.time.get_ticks()

# Variables de score
score = 0
coins = 0
stars = 0

# Boucle principale
game_over_font = pygame.font.SysFont("Arial", 72)
running = True
while running:
    dt = clock.tick(60)  # Limite à 60 FPS

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

    if countdown_left(game_start_ms) > 0:
        enemies.update()
        plantes_group.update()

        cam_x = max(0, player.rect.centerx - SCREEN_W // 2)
        cam_x = min(cam_x, level.width - SCREEN_W)

        screen.fill((135, 206, 235))  # ciel bleu
        level.draw(screen, cam_x)
        for group in (bricks, enemies, spikes, collectibles, plantes_group):
            group.draw(screen)
        screen.blit(player.image, (player.rect.x - cam_x, player.rect.y))

        sec = countdown_left(game_start_ms) // 1000 + 1
        countdown_text = pygame.font.SysFont(None, 72).render(str(sec), True, (255, 0, 0))
        screen.blit(countdown_text, countdown_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))

        pygame.display.flip()
        continue

    # Mise à jour
    plats = level.get_platforms()
    player.update(plats)
    for group in (bricks, enemies, spikes, collectibles, plantes_group):
        group.update()

    # Collision briques
    for e in enemies:
        if pygame.sprite.collide_rect(player, e) and e.alive:
            if player.vel_y > 0 and player.rect.bottom <= e.rect.top + 10:
                e.kill_enemy()
                player.vel_y = -10
            else:
                player.lose_life()
                if player.lives <= 0:
                    show_game_over()
                    running = False
                break

    # --- Collisions pics/plantes ---
    for group in (spikes, plantes_group):
        if pygame.sprite.spritecollide(player, group, False):
            player.lose_life()
            if player.lives <= 0:
                show_game_over()
                running = False
            break

    # --- Briques & Collectibles ---
    for b in bricks:
        if b.rect.colliderect(player.rect) and player.is_jumping_up:
            item = b.break_brick()
            if item:
                collectibles.add(item)
                if isinstance(item, Coin):
                    score += 10
                    coins += 1
                elif isinstance(item, Star):
                    score += 50
                    stars += 1


    # Passage de niveau
    for p in plats:
        if getattr(p, "type", None) == "flag" and player.rect.colliderect(p.rect):
            current_level_id += 1
            if current_level_id >= len(level_files):
                running = False
                break
            level = Level(level_files[current_level_id], "tiles.png")
            bricks, enemies, spikes, plantes_group = build_world_for_level(current_level_id)
            collectibles.empty()
            spawn_x = 100
            player.rect.topleft = (spawn_x, find_spawn(level, spawn_x))
            break

    # Calcul du temps écoulé en minutes:secondes, sans le compte à rebours
    elapsed_ms = max(0, pygame.time.get_ticks() - (game_start_ms + COUNTDOWN_MS))
    elapsed_sec = elapsed_ms // 1000
    minutes = elapsed_sec // 60
    seconds = elapsed_sec % 60


    # Caméra
    cam_x = max(0, player.rect.centerx - SCREEN_W // 2)
    cam_x = min(cam_x, level.width - SCREEN_W)

    # Affichage
    screen.fill((135, 206, 235))
    level.draw(screen, cam_x)
    for group in (bricks, enemies, spikes, collectibles, plantes_group):
        for s in group:
            screen.blit(s.image, (s.rect.x - cam_x, s.rect.y))
    screen.blit(player.image, (player.rect.x - cam_x, player.rect.y))

    # HUD
    screen.blit(font.render(f"Score : {score}", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"Pièces : {coins}", True, (255, 215, 0)), (10, 40))
    screen.blit(font.render(f"Étoiles : {stars}", True, (255, 215, 0)), (10, 70))
    screen.blit(font.render(f"Vies : {player.lives}", True, (255, 0, 0)), (10, 100))
    screen.blit(font.render(f"Temps : {minutes:02}:{seconds:02}", True, (0, 0, 0)), (10, 100))


    pygame.display.flip()

pygame.quit()