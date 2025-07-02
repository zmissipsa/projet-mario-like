import pygame

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []

        # Génère 3 images de flammes différentes
        for i in range(3):
            surf = pygame.Surface((20, 40), pygame.SRCALPHA)
            color = (255, 100 + i * 50, 0)
            pygame.draw.ellipse(surf, color, [0, 0, 20, 40])
            self.images.append(surf)

        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame = 0
        self.frame_timer = 0

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= 10:
            self.frame_timer = 0
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
