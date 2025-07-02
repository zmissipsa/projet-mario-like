import pygame
from player import Player
from level import Level
from sprites import Brick, Coin, Star, Spritesheet
from enemy import Enemy, Spike, PiranhaPlant, BlueGoomba, FlyingGhost, FallingEnemy
from menu import menu
from sprites import MovingPlatform
import sys



# Constantes
SCREEN_W, SCREEN_H = 1200, 600
GROUND_Y = 500

COUNTDOWN_MS = 3000 # 3 secondes avant démarrage du jeu

# Initialiser sons du jeu
try:
    pygame.mixer.init()
    hit_sound = pygame.mixer.Sound("assets/sounds/bump.ogg")            # Quand joueur touche un ennemi
    game_over_sound = pygame.mixer.Sound("assets/sounds/death.wav")     # Quand joueur perd
    coin_sound = pygame.mixer.Sound("assets/sounds/coin.ogg")           # Coin
    win_sound = pygame.mixer.Sound("assets/sounds/win.mp3")
except Exception as e:
    hit_sound = None
    game_over_sound = None
    coin_sound = None
    win_sound = None
    print("[WARNING] Le son de saut n'a pas pu être chargé :", e)

# Initialisation Pygame et fenêtre
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Mario-like")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


# Chargement des spritesheets
tiles_sheet = Spritesheet("assets/images/tiles.png")
enemy_sheet = Spritesheet("assets/images/characters.gif")
heart_sheet = Spritesheet("assets/images/coeur.png")

def build_world_for_level(level_idx):
    bricks, enemies, spikes = (pygame.sprite.Group() for _ in range(3))
    plantes_group = pygame.sprite.Group()  # Groupe plantes Piranha
    moving_platforms = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

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
    elif level_idx == 2:
        bricks.add(
            Brick(350, 300, tiles_sheet, True, "coin"),
            Brick(500, 250, tiles_sheet, True, "star"),
            Brick(700, 250, tiles_sheet, True, "coin"),
            Brick(1100, 200, tiles_sheet, True, "star"),
            Brick(3325, 50, tiles_sheet, True, "coin"),
        )

        tuyaux = [
            (3300, 200)
        ]

        tuyaux_plantes_indices = [0]

        plante_height = 38  

        for i in tuyaux_plantes_indices:
            x, y = tuyaux[i]
            plante = PiranhaPlant(x + 25, y - plante_height, enemy_sheet)
            plantes_group.add(plante)
            # Rampe mobile 1
        moving_platforms.add(MovingPlatform(300, 420, tiles_sheet, 300, 600))  # Position ajustée au-dessus de la lave

        # Rampe mobile 2
        moving_platforms.add(MovingPlatform(650, 380, tiles_sheet, 650,1000))

        # Rampe mobile 3
        moving_platforms.add(MovingPlatform(1000, 340, tiles_sheet, 1000, 1400))
        
        # === Fantômes volants ===
        for x in [1600, 2000]:  # ou même juste un seul
            ghost = FlyingGhost(x, 450, enemy_sheet, enemies, all_sprites)
            enemies.add(ghost)
            all_sprites.add(ghost)



        # Spikes invisibles pour représenter la lave en-dessous
        for x in range(300, 1400, 50): 
            spike = Spike(x, GROUND_Y, enemy_sheet)
            spike.image.set_alpha(0)  # invisible
            spikes.add(spike)
        for x in range(2300, 2700, 50): 
            spike = Spike(x, GROUND_Y, enemy_sheet)
            spike.image.set_alpha(0)  # invisible
            spikes.add(spike)

       

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

        enemy_positions = [
            (2000, GROUND_Y, 400, 700),
            (1500, GROUND_Y, 700, 1000),
            (1100, GROUND_Y, 1000, 1250),  
            (1800, GROUND_Y, 1300, 1500),
        ]

        for x, y, left, right in enemy_positions:
            if x != 1800 and x!=1100:
                enemies.add(Enemy(x, y, left, right, enemy_sheet))

        enemies.add(BlueGoomba(1300, GROUND_Y - 35, enemy_sheet, 1000, 1400))

        spikes.add(
            Spike(400, GROUND_Y, enemy_sheet),
            Spike(250, GROUND_Y, enemy_sheet),
            Spike(600, GROUND_Y, enemy_sheet),
            Spike(800, GROUND_Y, enemy_sheet),
            Spike(1000, GROUND_Y, enemy_sheet),
            Spike(1200, GROUND_Y, enemy_sheet),
        )
        tuyaux = [
            (1500, 450),  
            (1600, 400),  
            (1700, 350),  
            (1800, 300),  
            (1900, 350),  
            (2000, 400),  
            (2100, 450)   
        ]

        tuyaux_plantes_indices = [0, 3, 5, 6]

        plante_height = 38  

        for i in tuyaux_plantes_indices:
            x, y = tuyaux[i]
            plante = PiranhaPlant(x + 25, y - plante_height, enemy_sheet)
            plantes_group.add(plante)

    return bricks, enemies, spikes, plantes_group, moving_platforms, all_sprites






def find_spawn(level, x_world):
    """Trouve la meilleure position y pour faire apparaître le joueur à la coordonnée x."""
    best_top = SCREEN_H
    for p in level.get_platforms():
        if p.is_solid and p.rect.left <= x_world <= p.rect.right:
            best_top = min(best_top, p.rect.top)
    if best_top == SCREEN_H:
        best_top = GROUND_Y - 50
    return best_top - 48

def countdown_left(level_start_ms):
    return max(0, COUNTDOWN_MS - (pygame.time.get_ticks() - level_start_ms))

def show_game_over():
    text = pygame.font.SysFont("Arial", 72).render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, text.get_rect(center=(SCREEN_W//2, SCREEN_H//2)))
    pygame.display.flip()
    pygame.time.wait(3000)

def show_you_win():
    text = pygame.font.SysFont("Arial", 72).render("YOU WIN", True, (255, 0, 0))
    screen.blit(text, text.get_rect(center=(SCREEN_W//2, SCREEN_H//2)))
    pygame.display.flip()
    pygame.time.wait(2000)

def level_screen(lvl_id, screen, score, time_ms):         #ecran de fin de niveau
    font_title = pygame.font.SysFont("Arial", 64)
    font_small = pygame.font.SysFont("Arial", 36)

    minutes = (time_ms // 1000) // 60
    seconds = (time_ms // 1000) % 60

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    return  # Passe au niveau suivant
        
        screen.fill((135, 206, 235))  # Fond bleu ciel
        title = font_title.render(f"Niveau {lvl_id} terminé ", True, (255, 255, 0))
        score_text = font_small.render(f"Score total : {score}", True, (255, 255, 255))
        time_text = font_small.render(f"Temps : {minutes:02}:{seconds:02}", True, (255, 255, 255))
        hint_text = font_small.render("Appuie sur Entrée pour continuer", True, (0, 0, 0))

        screen.blit(title, title.get_rect(center=(SCREEN_W // 2, 150)))
        screen.blit(score_text, score_text.get_rect(center=(SCREEN_W // 2, 250)))
        screen.blit(time_text, time_text.get_rect(center=(SCREEN_W // 2, 300)))
        screen.blit(hint_text, hint_text.get_rect(center=(SCREEN_W // 2, 400)))

        pygame.display.flip()
        clock.tick(60)

# Menu pause
def pause_menu(screen):
    font_title = pygame.font.SysFont("Arial", 64)
    font_small = pygame.font.SysFont("Arial", 36)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    return  # revenir au jeu
                
        screen.fill((135, 206, 235))  # Fond bleu ciel
        title = font_title.render(f"Pause", True, (255, 255, 225))
        hint_text = font_small.render("Appuie sur Entrée pour continuer", True, (0, 0, 0))

        screen.blit(title, title.get_rect(center=(SCREEN_W // 2, 150)))
        screen.blit(hint_text, hint_text.get_rect(center=(SCREEN_W // 2, 400)))
        
        pygame.display.flip()

def run_game():
    # Chargement des niveaux
    level_files = ["niveau1.txt", "niveau2.txt", "niveau3.txt"]
    current_level_id = 0

    # Initialisation du niveau
    level = Level(level_files[current_level_id], "tiles.png")
    bricks, enemies, spikes, plantes_group, moving_platforms, all_sprites = build_world_for_level(current_level_id)
    collectibles = pygame.sprite.Group()

    spawn_x = 100
    player = Player(spawn_x, find_spawn(level, spawn_x))
    player.start_position = player.rect.topleft
    game_start_ms = pygame.time.get_ticks()  # le vrai départ de la partie
    level_enter_ms = game_start_ms           # pour le compte à rebours du niveau 1


    # Variables de score
    score = 0
    coins = 0
    stars = 0

    running = True
    while running:
        dt = clock.tick(60)  # Limite à 60 FPS
        plats = list(level.get_platforms()) + list(moving_platforms)
        for s in all_sprites:
            if isinstance(s, FallingEnemy):
                s.update(plats)
            else:
                s.update()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "quit"
            
            # Menu Pause
            if ev.type == pygame.KEYDOWN:                    
                if ev.key == pygame.K_p:
                    summary_start = pygame.time.get_ticks()     #temps avant pause
                    pause_menu(screen)
                    summary_end = pygame.time.get_ticks()     #temps apres pause
                    
                    #mise a jour du temps
                    game_start_ms += summary_end - summary_start

        if countdown_left(level_enter_ms) > 0:
            enemies.update()
            plantes_group.update()
    

            cam_x = max(0, player.rect.centerx - SCREEN_W // 2)
            cam_x = min(cam_x, level.width - SCREEN_W)

            if current_level_id == 2:
                screen.fill((20, 20, 40))
            else:
                screen.fill((135, 206, 235))

            level.draw(screen, cam_x)
            for group in (bricks, enemies, spikes, collectibles, plantes_group):
                group.draw(screen)
            moving_platforms.draw(screen)  # Affichage rampes

            screen.blit(player.image, (player.rect.x - cam_x, player.rect.y))

            sec = countdown_left(game_start_ms) // 1000 + 1
            countdown_text = pygame.font.SysFont(None, 72).render(str(sec), True, (255, 0, 0))
            screen.blit(countdown_text, countdown_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))

            pygame.display.flip()
            continue
        
        plats = list(level.get_platforms()) + list(moving_platforms)
        player.update(plats)
        
        # 1. Met à jour toutes les rampes mobiles
        for plat in moving_platforms:
            plat.update()

        # Si Mario est sur une plateforme mobile, il doit suivre son mouvement
        if player.attached_platform:
            delta_x = player.attached_platform.rect.x - player.attached_platform.prev_x
            player.rect.x += delta_x


        # 3. Collision avec les rampes pour s’y attacher
        player.attached_platform = None
        for plat in moving_platforms:
            if pygame.sprite.collide_rect(player, plat):
                if abs(player.rect.bottom - plat.rect.top) <= 6 and player.vel_y >= 0:
                    player.rect.bottom = plat.rect.top
                    player.vel_y = 0
                    player.attached_platform = plat
                    break  # une seule rampe à la fois


        for group in (bricks, spikes, collectibles, plantes_group):
            group.update()

        for e in enemies:
            if isinstance(e, FallingEnemy):
                e.update(plats)
            else:
                e.update()



        # Collision enemies
        for e in enemies:
            if pygame.sprite.collide_rect(player, e) and getattr(e, "alive", True):
                if player.vel_y > 0 and player.rect.bottom - e.rect.top < 20:
                    if isinstance(e, (BlueGoomba, Enemy, FallingEnemy, FlyingGhost)):
                        e.crush()
                        if hasattr(e, 'crush'):
                            e.crush()
                        else:
                            e.kill()
                    player.vel_y = -10
                else:
                    if hit_sound:
                        hit_sound.play()
                    player.lose_life()
                    if player.lives <= 0:
                        if game_over_sound:
                            game_over_sound.play()
                        show_game_over()
                        return "menu"
                break


        # Collisions pics/plantes
        for group in (spikes, plantes_group):
            if pygame.sprite.spritecollide(player, group, False):
                if hit_sound:
                    hit_sound.play()
                player.lose_life()
                if player.lives <= 0:
                    if game_over_sound:
                        game_over_sound.play()
                    show_game_over()
                    return "menu"
                break

        # Briques
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
                    if coin_sound:
                        coin_sound.play()

        # Passage de niveau
        for p in plats:
            if getattr(p, "type", None) == "flag" and player.rect.colliderect(p.rect):
                current_level_id += 1
                if current_level_id >= len(level_files):
                    if win_sound:
                        win_sound.play()
                    show_you_win()
                    return "menu"
                else:
                    summary_start = pygame.time.get_ticks()     #temps avant la page de fin de niveau
                    level_screen(current_level_id, screen, score, pygame.time.get_ticks() - game_start_ms)
                    summary_end = pygame.time.get_ticks()     #temps apres la page de fin de niveau
                    
                    #mise a jour du temps
                    game_start_ms += summary_end - summary_start

                    level = Level(level_files[current_level_id], "tiles.png")
                    bricks, enemies, spikes, plantes_group, moving_platforms, all_sprites = build_world_for_level(current_level_id)

                    collectibles.empty()
                    spawn_x = 100
                    player.rect.topleft = (spawn_x, find_spawn(level, spawn_x))
                    level_enter_ms = pygame.time.get_ticks()
                    player.lives += 1
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
        if current_level_id == 2:
            screen.fill((20, 20, 40))
        else:
            screen.fill((135, 206, 235))
            
        for s in all_sprites:
            screen.blit(s.image, (s.rect.x - cam_x, s.rect.y))


        level.draw(screen, cam_x)
        for group in (bricks, enemies, spikes, collectibles, plantes_group):
            for s in group:
                screen.blit(s.image, (s.rect.x - cam_x, s.rect.y))
        for plat in moving_platforms:
            screen.blit(plat.image, (plat.rect.x - cam_x, plat.rect.y))

        screen.blit(player.image, (player.rect.x - cam_x, player.rect.y))

        # HUD
        screen.blit(font.render(f"Score : {score}", True, (0, 0, 0)), (10, 10))
        screen.blit(font.render(f"Pièces : {coins}", True, (255, 215, 0)), (10, 40))
        screen.blit(font.render(f"Étoiles : {stars}", True, (255, 215, 0)), (10, 70))
        
        # les vies du joueur
        heart_img = pygame.transform.scale(heart_sheet.get_image(0,0,511,511), (32, 32))
        for i in range(player.lives):
            screen.blit(heart_img, (10 + i * 40, 100))  # espace entre les cœurs


        screen.blit(font.render(f"Temps : {minutes:02}:{seconds:02}", True, (0, 0, 0)), (10, 130))

        pygame.display.flip()


while True:
    menu(screen)
    result = run_game()
    if result == "quit":
        break