import pygame
import sys
from sprites import Spritesheet

SCREEN_W, SCREEN_H = 1200, 600
clock = pygame.time.Clock()

def menu(screen):
    # Initialiser le mixeur audio (fait ici, après pygame.init())
    pygame.mixer.init()
    
    # Charger la musique du menu (remplace par le chemin correct de ton fichier)
    pygame.mixer.music.load("assets/sounds/main_theme.ogg")
    pygame.mixer.music.play(-1)  # jouer en boucle (-1)

    # Charger l'image Mario ici, après que l'écran soit initialisé
    mario_img = pygame.image.load("assets/images/mario.png").convert_alpha()
    mario_img = pygame.transform.scale(mario_img, (150, 200))

    # Charger l'image du curseur 
    
    index_img = pygame.transform.scale(Spritesheet("assets/images/tiles.png").get_image(228, 24, 8, 8), (30, 30))

    font = pygame.font.SysFont("Arial", 48)
    font_small = pygame.font.SysFont("Arial", 36)

    options = ["Démarrer", "Quitter"]
    selected_index = 0

    def draw_menu():
        screen.fill((135, 206, 235))  # Fond bleu ciel

        # Dessiner Mario au centre haut
        mario_rect = mario_img.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3))
        screen.blit(mario_img, mario_rect)

        # Titre
        title = font.render("Mario-like", True, (255, 0, 0))
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 50))

        # Options du menu
        for i, text in enumerate(options):
            rendered = font_small.render(f"{text}", True, (0, 0, 0))
            text_x = SCREEN_W // 2 - rendered.get_width() // 2
            text_y = SCREEN_H // 2 + i * 50
            screen.blit(rendered, (text_x, text_y))
            if i == selected_index:
                screen.blit(index_img, (text_x - 40, text_y + 5))



    pygame.key.set_repeat(300, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # fleche du bas
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_UP:  # fleche du haut 
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:     # entree
                    pygame.mixer.music.stop()
                    if selected_index == 0:
                        return  # Démarrer
                    elif selected_index == 1:
                        pygame.quit()
                        sys.exit()

        draw_menu()
        pygame.display.flip()
        clock.tick(60)




