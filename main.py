import pygame
from player  import Player
from level   import Level
from sprites import Brick, Coin, Star, Spritesheet
from enemy   import Enemy, Spike

# ------------------------------------------------------ #
SCREEN_W, SCREEN_H = 1200, 600
GROUND_Y           = 500
COUNTDOWN_MS       = 10000        # 5 s avant de jouer

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Mario‑like")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont(None, 36)

tiles_sheet = Spritesheet("assets/images/tiles.png")
enemy_sheet = Spritesheet("assets/images/characters.gif")

# ------------------------------------------------------ #
def build_world_for_level(level_idx):
    bricks, enemies, spikes = (pygame.sprite.Group() for _ in range(3))

    
    if level_idx == 0:   # objets seulement dans le niveau 1
        bricks.add(
            Brick(300,250,tiles_sheet,True,"coin"),
            Brick(500,250,tiles_sheet,True,"coin"),
            Brick(700,300,tiles_sheet,True,"star"),
            Brick(900,350,tiles_sheet,True,"star"),
        )
        enemies.add(
            Enemy(400,GROUND_Y,400,600,enemy_sheet),
            Enemy(700,GROUND_Y,650,1100,enemy_sheet),
        )
        spikes.add(
            Spike(1050,GROUND_Y,enemy_sheet),
            Spike( 200,GROUND_Y,enemy_sheet),
        )
    if level_idx == 1:   # objets seulement dans le niveau 2
        bricks.add(
            Brick(300,250,tiles_sheet,True,"coin"),
            Brick(500,250,tiles_sheet,True,"star"),
            Brick(700,250,tiles_sheet,True,"coin"),
            Brick(1100,250,tiles_sheet,True,"star"),
            Brick(1400,350,tiles_sheet,True,"star"),
            Brick(1800,150,tiles_sheet,True,"coin"),
            Brick(2000,200,tiles_sheet,True,"coin"),
            
        )
        enemies.add(
            Enemy(2000,GROUND_Y,400,700,enemy_sheet),
            Enemy(1500,GROUND_Y,700,1000,enemy_sheet),
            Enemy(1100,GROUND_Y,1000,1250,enemy_sheet),
            Enemy(1800,GROUND_Y,1300,1500,enemy_sheet),
        )
        spikes.add(
            Spike(400,GROUND_Y,enemy_sheet),
            Spike( 250,GROUND_Y,enemy_sheet),
            Spike(600,GROUND_Y,enemy_sheet),
            Spike( 800,GROUND_Y,enemy_sheet),
            Spike(1000,GROUND_Y,enemy_sheet),
            Spike(1200,GROUND_Y,enemy_sheet),
        )
    return bricks, enemies, spikes

# ------------------------------------------------------ #
def find_spawn(level, x_world):
    best_top = SCREEN_H
    for p in level.get_platforms():
        if p.is_solid and p.rect.left <= x_world <= p.rect.right:
            best_top = min(best_top, p.rect.top)
    if best_top == SCREEN_H:
        best_top = GROUND_Y - 50
    return best_top - 48

def countdown_left(start_ms):
    """ms restantes avant GO (0 si fini)."""
    return max(0, COUNTDOWN_MS - (pygame.time.get_ticks() - start_ms))

# ------------------------------------------------------ #
level_files      = ["niveau1.txt", "niveau2.txt"]
current_level_id = 0

level   = Level(level_files[current_level_id], "tiles.png")
bricks, enemies, spikes = build_world_for_level(current_level_id)
collectibles = pygame.sprite.Group()

spawn_x = 100
player  = Player(spawn_x, find_spawn(level, spawn_x))

level_start_ms = pygame.time.get_ticks()   # démarre le décompte

score = coins = stars = 0

# ====================================================== #
running = True
while running:
    dt = clock.tick(60)                    # temps frame (ms)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

    # ---------- PHASE COMPTE À REBOURS ---------------- #
    if countdown_left(level_start_ms) > 0:
        # tu peux commenter la ligne suivante si tu ne veux PAS
        # que les ennemis se déplacent pendant le décompte.
        enemies.update()

        # Caméra fixe centrée sur Mario
        cam_x = max(0, player.rect.centerx - SCREEN_W//2)
        cam_x = min(cam_x, level.width - SCREEN_W)

        screen.fill((135,206,235))
        level.draw(screen, cam_x)
        for grp in (bricks, enemies, spikes, collectibles):
            for s in grp:
                screen.blit(s.image, (s.rect.x - cam_x, s.rect.y))
        screen.blit(player.image, (player.rect.x - cam_x, player.rect.y))

        sec = countdown_left(level_start_ms) // 1000 + 1   # 4999→5
        txt = pygame.font.SysFont(None, 72).render(str(sec), True, (255,0,0))
        screen.blit(txt, txt.get_rect(center=(SCREEN_W//2, SCREEN_H//2)))
        pygame.display.flip()
        continue                    # on saute la mise à jour du joueur

    # ---------- UPDATE JEU NORMAL --------------------- #
    plats = level.get_platforms()
    player.update(plats)
    for grp in (bricks, enemies, spikes, collectibles):
        grp.update()

    # -- briques cassables --
    for b in bricks:
        if b.rect.colliderect(player.rect) and player.is_jumping_up:
            item = b.break_brick()
            if item:
                collectibles.add(item)
                if isinstance(item, Coin):
                    score += 10; coins += 1
                elif isinstance(item, Star):
                    score += 50; stars += 1

    # -- collisions ennemis --
    for e in enemies:
        if pygame.sprite.collide_rect(player, e) and e.alive:
            if player.vel_y > 0 and player.rect.bottom <= e.rect.top + 10:
                e.kill_enemy(); player.vel_y = -10
            else:
                player.rect.topleft = (spawn_x, find_spawn(level, spawn_x))

    # -- collisions pics --
    if pygame.sprite.spritecollide(player, spikes, False):
        txt = pygame.font.SysFont("Arial",72).render("GAME OVER",True,(255,0,0))
        screen.blit(txt,(400,250)); pygame.display.flip(); pygame.time.wait(2000)
        break

    # -- passage drapeau --
    for p in plats:
        if getattr(p,"type",None)=="flag" and player.rect.colliderect(p.rect):
            current_level_id += 1
            if current_level_id >= len(level_files):
                running = False
                break

            level = Level(level_files[current_level_id], "tiles.png")
            bricks, enemies, spikes = build_world_for_level(current_level_id)
            collectibles.empty()
            spawn_x = 100
            player.rect.topleft = (spawn_x, find_spawn(level, spawn_x))
            level_start_ms = pygame.time.get_ticks()       # nouveau décompte
            break

    # ---------- CAMERA & DRAW ------------------------- #
    cam_x = max(0, player.rect.centerx - SCREEN_W//2)
    cam_x = min(cam_x, level.width - SCREEN_W)

    screen.fill((135,206,235))
    level.draw(screen, cam_x)
    for grp in (bricks, enemies, spikes, collectibles):
        for s in grp:
            screen.blit(s.image, (s.rect.x - cam_x, s.rect.y))
    screen.blit(player.image, (player.rect.x - cam_x, player.rect.y))

    # HUD
    screen.blit(font.render(f"Score : {score}", True,(0,0,0)), (10,10))
    screen.blit(font.render(f"Pièces : {coins}", True,(255,215,0)), (10,40))
    screen.blit(font.render(f"Étoiles : {stars}",True,(255,255,255)), (10,70))

    pygame.display.flip()

pygame.quit()
