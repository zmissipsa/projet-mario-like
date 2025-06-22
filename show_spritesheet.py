import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))  # adapte la taille si besoin
pygame.display.set_caption("Afficher spritesheet et coordonnées")

spritesheet = pygame.image.load('assets/images/characters.gif').convert_alpha()  # adapte le nom et l'extension

running = True
font = pygame.font.SysFont(None, 24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # fond noir
    screen.blit(spritesheet, (0, 0))  # affiche la spritesheet entière en haut à gauche

    # Récupérer la position de la souris
    x, y = pygame.mouse.get_pos()

    # Affiche la position de la souris en haut à gauche de l'écran
    text = font.render(f"Mouse position: ({x}, {y})", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()

