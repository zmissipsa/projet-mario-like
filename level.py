import pygame
import os
from sprites import Spritesheet

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image, p_type="ground", is_solid=1):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = p_type
        self.is_solid = bool(is_solid)

class Level:
    def __init__(self, tile_map_txt, tile_sheet_png):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()

        self.spritesheet = Spritesheet(os.path.join("assets", "images", tile_sheet_png))
        self.load_level(os.path.join("levels", tile_map_txt))

    def load_level(self, txt_path):
        with open(txt_path, 'r') as f:
            for line in f:
                if not line.strip() or line.startswith('#'):
                    continue
                parts = line.strip().split(',')

                if parts[0] == "enemy":
                    x, y, left_bound, right_bound = map(int, parts[1:5])
                    speed = int(parts[5]) if len(parts) > 5 else 2
                    from enemy import Enemy
                    enemy_spritesheet = Spritesheet("./assets/images/characters.gif")
                    enemy = Enemy(x, y, left_bound, right_bound, spritesheet=enemy_spritesheet, speed=speed)
                    self.enemies.add(enemy)
                    continue

                if parts[0] == "spike":
                    x, y = map(int, parts[1:3])
                    from enemy import Spike
                    spike_spritesheet = Spritesheet("./assets/images/characters.gif")
                    spike = Spike(x, y, spike_spritesheet)
                    self.spikes.add(spike)
                    continue

                if len(parts) < 8:
                    continue

                x, y, w, h, sx, sy, sw, sh = map(int, parts[:8])
                is_solid = int(parts[8]) if len(parts) > 8 else 1
                p_type = parts[9] if len(parts) > 9 else "ground"

                sprite = self.spritesheet.get_image(sx, sy, sw, sh)
                sprite = pygame.transform.scale(sprite, (w, h))
                platform = Platform(x, y, sprite, p_type, is_solid)
                self.platforms.add(platform)

    def draw(self, surface):
        self.platforms.draw(surface)

    def get_platforms(self):
        return self.platforms

    def get_enemies(self):
        return self.enemies

    def get_spikes(self):
        return self.spikes

