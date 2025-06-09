import pygame
import time
from missile import Missile

class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("Astrocrash_game/assets/ship.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = pygame.math.Vector2(0, -1)  # Mặc định hướng lên
        self.angle = 0
        self.speed = 3
        self.last_fire = 0

    def update(self, keys=None):
        dx, dy = 0, 0
        if keys:
            if keys[pygame.K_LEFT]:
                dx = -self.speed
                self.direction = pygame.math.Vector2(-1, 0)
                self.angle = 90
            elif keys[pygame.K_RIGHT]:
                dx = self.speed
                self.direction = pygame.math.Vector2(1, 0)
                self.angle = -90
            elif keys[pygame.K_UP]:
                dy = -self.speed
                self.direction = pygame.math.Vector2(0, -1)
                self.angle = 0
            elif keys[pygame.K_DOWN]:
                dy = self.speed
                self.direction = pygame.math.Vector2(0, 1)
                self.angle = 180

        # Cập nhật vị trí mới và giới hạn trong màn hình
        new_x = self.rect.centerx + dx
        new_y = self.rect.centery + dy
        half_w = self.rect.width // 2
        half_h = self.rect.height // 2
        new_x = max(half_w, min(800 - half_w, new_x))
        new_y = max(half_h, min(600 - half_h, new_y))
        self.rect.center = (new_x, new_y)

        # Xoay sprite theo hướng
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def fire(self):
        self.last_fire = time.time()
        return Missile(self.rect.center, self.direction)

    def can_fire(self):
        return time.time() - self.last_fire > 0.25
