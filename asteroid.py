import pygame, random

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("Astrocrash_game/assets/asteroid.png").convert_alpha()
        self.reset()

    def reset(self):
        # Chọn tỉ lệ ngẫu nhiên để tạo viên to viên nhỏ
        scale_factor = random.choice([0.5, 0.7, 1, 1.2])
        width = int(self.original_image.get_width() * scale_factor)
        height = int(self.original_image.get_height() * scale_factor)
        self.image = pygame.transform.smoothscale(self.original_image, (width, height))
        self.rect = self.image.get_rect(center=(random.randint(0, 800), random.randint(-100, -40)))
        self.base_speed_y = random.uniform(0.5, 1.2)
        self.speed_x = random.uniform(-0.8, 0.8)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        elapsed = pygame.time.get_ticks() / 1000  # thời gian chạy game
        speed_multiplier = 1 + (elapsed // 15) * 0.2  # tăng mỗi 15s
        final_speed_y = min(self.base_speed_y * speed_multiplier, 4.0)  # Giới hạn tốc độ tối đa

        self.rect.centerx += self.speed_x
        self.rect.centery += final_speed_y

        # Nếu rơi xuống dưới màn hình thì reset (tái sinh)
        if self.rect.top > 600:
            self.reset()
