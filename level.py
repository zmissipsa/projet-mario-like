import pygame
import os
from sprites import Spritesheet

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, p_type="ground", is_solid=True):
        super().__init__()
        self.image     = sprite
        self.rect      = self.image.get_rect(topleft=(x, y))
        self.type      = p_type      
        self.is_solid  = is_solid    

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
                parts = line.strip().split(',')
                x, y, w, h, sx, sy, sw, sh = map(int, parts[:8])
                is_solid = int(parts[8])if len(parts) > 8 else 1
                p_type   = parts[9]       if len(parts) > 9 else "ground"

                
                #extraire le sprite correspondant du spritesheet
                sprite = self.spritesheet.get_image(sx, sy, sw, sh)
                
                #redimensionner
                sprite = pygame.transform.scale(sprite, (w, h))
                
                #creer la plateforme et l'ajouter au groupe
                platform = Platform(x, y, sprite, p_type, is_solid)
                self.platforms.add(platform)
    
    def draw(self, surface):
        self.platforms.draw(surface)
    
    def get_platforms(self):
        return self.platforms