import pygame
import time

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.image.load("Astrocrash_game/assets/explosion.png").convert_alpha()
        self.rect = self.image.get_rect(center=center)
        self.spawn_time = time.time()

    def update(self):
        if time.time() - self.spawn_time > 0.3:
            self.kill()
