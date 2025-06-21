import pygame, os
from sprites import Spritesheet

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image, p_type="ground", is_solid=1):
        super().__init__()
        self.image = image
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.type      = p_type        # "ground", "flag", etc.
        self.is_solid  = bool(is_solid)

class Level:
    """
    offset_x : décalage horizontal appliqué à tous les blocs / ennemis.
    """
    def __init__(self, tile_map_txt, tile_sheet_png, offset_x=0):
        self.platforms = pygame.sprite.Group()
        self.enemies   = pygame.sprite.Group()
        self.spikes    = pygame.sprite.Group()
        self.offset_x  = offset_x
        self.width     = 0

        self.spritesheet = Spritesheet(os.path.join("assets", "images",
                                                    tile_sheet_png))
        self.load_level(os.path.join("levels", tile_map_txt))

    # ------------------------------------------------------------------
    def load_level(self, txt_path):
        with open(txt_path, "r") as f:
            for line in f:
                ln = line.strip()
                if not ln or ln.startswith("#"):
                    continue
                parts = ln.split(",")

                # -- ennemis ------------------------------------------------
                if parts[0] == "enemy":
                    x, y, left, right = map(int, parts[1:5])
                    speed = int(parts[5]) if len(parts) > 5 else 2
                    from enemy import Enemy
                    enemy_sheet = Spritesheet("assets/images/characters.gif")
                    self.enemies.add(
                        Enemy(x+self.offset_x, y,
                              left+self.offset_x, right+self.offset_x,
                              spritesheet=enemy_sheet, speed=speed))
                    continue

                # -- pics ---------------------------------------------------
                if parts[0] == "spike":
                    x, y = map(int, parts[1:3])
                    from enemy import Spike
                    spike_sheet = Spritesheet("assets/images/characters.gif")
                    self.spikes.add(
                        Spike(x+self.offset_x, y, spike_sheet))
                    continue

                # -- blocs / plateformes -----------------------------------
                if len(parts) < 8:
                    continue
                x, y, w, h, sx, sy, sw, sh = map(int, parts[:8])
                is_solid = int(parts[8]) if len(parts) > 8 else 1
                p_type   = parts[9] if len(parts) > 9 else "ground"

                sprite = self.spritesheet.get_image(sx, sy, sw, sh)
                sprite = pygame.transform.scale(sprite, (w, h))
                self.platforms.add(
                    Platform(x+self.offset_x, y, sprite, p_type, is_solid))

                self.width = max(self.width, x+self.offset_x + w)

    # ------------------------------------------------------------------
    def draw(self, surf, cam_x=0):
        for p in self.platforms:
            if p.rect.right < cam_x or p.rect.left > cam_x + surf.get_width():
                continue
            surf.blit(p.image, (p.rect.x - cam_x, p.rect.y))

    def get_platforms(self): return self.platforms
    def get_enemies(self):   return self.enemies
    def get_spikes(self):    return self.spikes
