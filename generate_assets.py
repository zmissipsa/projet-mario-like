import pygame
import os
import math

# Initialisation de Pygame
pygame.init()

# Création dossier assets/images si n'existe pas
os.makedirs("assets/images", exist_ok=True)

# Dimensions des images
size = (64, 64)

# --- Création de la pièce (cercle jaune) ---
coin_surface = pygame.Surface(size, pygame.SRCALPHA)
pygame.draw.circle(coin_surface, (255, 215, 0), (32, 32), 25)  # Cercle jaune doré

# Sauvegarde de la pièce
pygame.image.save(coin_surface, "assets/images/coin.png")

# --- Création de l'étoile ---
star_surface = pygame.Surface(size, pygame.SRCALPHA)

# Fonction pour dessiner une étoile
def draw_star(surface, color, center, radius, points=5):
    angle = math.pi / points
    coords = []
    for i in range(2 * points):
        r = radius if i % 2 == 0 else radius / 2
        x = center[0] + r * math.sin(i * angle)
        y = center[1] - r * math.cos(i * angle)
        coords.append((x, y))
    pygame.draw.polygon(surface, color, coords)

draw_star(star_surface, (255, 215, 0), (32, 32), 25)

# Sauvegarde de l'étoile
pygame.image.save(star_surface, "assets/images/star.png")

print("Images créées dans assets/images/coin.png et star.png")

pygame.quit()
