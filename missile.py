import pygame

class Missile(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.image.load("Astrocrash_game/assets/missile.png").convert_alpha()
        
        # Xoay đầu đạn theo hướng
        angle = direction.angle_to(pygame.math.Vector2(0, -1))
        self.image = pygame.transform.rotate(self.image, angle)
        
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction.normalize()  # Hướng bay (Vector2)
        self.speed = 10

    def update(self):
        move = self.direction * self.speed
        self.rect.centerx += move.x
        self.rect.centery += move.y

        # Xóa nếu ra khỏi màn hình
        if (self.rect.right < 0 or self.rect.left > 800 or
            self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()
