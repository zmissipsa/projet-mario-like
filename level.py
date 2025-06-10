import pygame
import os
from sprites import Spritesheet

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

class Level:
    def __init__(self, tile_map_txt, tile_sheet_png):
        self.platforms = pygame.sprite.Group()
        
        #charger le spritesheet
        self.spritesheet = Spritesheet(os.path.join("assets", "images", tile_sheet_png))
        
        #charger les elements du lvl
        self.load_level(os.path.join("levels", tile_map_txt))
    
    def load_level(self, txt_path):
        #charger un fichier texte ou chaque ligne correspond a un bloc:
        #format attendu: x, y, width, height, sprite_x, sprite_y, sprite_w, sprite_h

        with open(txt_path, 'r') as f:
            for line in f :
                if not line.strip():
                    continue
                x, y, w, h, sx, sy, sw, sh = map(int, line.strip().split(','))
                
                #extraire le sprite correspondant du spritesheet
                sprite = self.spritesheet.get_image(sx, sy, sw, sh)
                
                #redimensionner
                sprite = pygame.transform.scale(sprite, (w, h))
                
                #créer la plateforme et l'ajouter au groupe
                platform = Platform(x, y, sprite)
                self.platforms.add(platform)
    
    def draw(self, surface):
        self.platforms.draw(surface)
    
    def get_platforms(self):
        self.platforms