import pygame
import sys

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

    font = pygame.font.SysFont("Arial", 48)
    font_small = pygame.font.SysFont("Arial", 36)

    def draw_menu():
        screen.fill((135, 206, 235))  # Fond bleu ciel

        # Dessiner Mario au centre haut
        mario_rect = mario_img.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3))
        screen.blit(mario_img, mario_rect)

        # Titre
        title = font.render("Mario-like", True, (255, 0, 0))
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 50))

        # Options du menu
        start_text = font_small.render("1. Démarrer", True, (0, 0, 0))
        quit_text = font_small.render("2. Quitter", True, (0, 0, 0))

        screen.blit(start_text, (SCREEN_W // 2 - start_text.get_width() // 2, SCREEN_H // 2))
        screen.blit(quit_text, (SCREEN_W // 2 - quit_text.get_width() // 2, SCREEN_H // 2 + 50))

    pygame.key.set_repeat(300, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Démarrer le jeu
                    pygame.mixer.music.stop()
                    return  # Sort de la fonction menu pour lancer le jeu
                elif event.key == pygame.K_2:  # Quitter
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

        draw_menu()
        pygame.display.flip()
        clock.tick(60)




