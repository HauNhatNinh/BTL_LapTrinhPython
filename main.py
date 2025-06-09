import pygame, sys, random
from ship import Ship
from asteroid import Asteroid
from missile import Missile
from explosion import Explosion

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Astrocrash")
clock = pygame.time.Clock()

# Tải ảnh nền
background = pygame.image.load("Astrocrash_game/assets/background.png").convert()


# Tải nhạc và âm thanh
boom_sound = pygame.mixer.Sound("Astrocrash_game/assets/boom.wav")
pygame.mixer.music.load("Astrocrash_game/assets/music.mp3")
pygame.mixer.music.play(-1)

# Sprite Groups
all_sprites = pygame.sprite.Group()
missiles = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Tạo tàu
ship = Ship(WIDTH // 2, HEIGHT // 2)
all_sprites.add(ship)

# Tạo thiên thạch ban đầu (giảm số lượng xuống 3)
for _ in range(3):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

# Điểm số và rung
score = 0
shake = 0
font = pygame.font.SysFont(None, 36)

# Thời gian sinh thêm thiên thạch
SPAWN_INTERVAL = 5000  # 5 giây
last_spawn_time = pygame.time.get_ticks()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    ship.update(keys)

    # Bắn tên lửa
    if keys[pygame.K_SPACE]:
        if ship.can_fire():
            missile = ship.fire()
            all_sprites.add(missile)
            missiles.add(missile)

    # Cập nhật sprite
    all_sprites.update()

    # Va chạm tên lửa với thiên thạch
    hits = pygame.sprite.groupcollide(missiles, asteroids, True, True)
    for hit in hits:
        boom_sound.play()
        score += 10
        exp = Explosion(hit.rect.center)
        all_sprites.add(exp)
        explosions.add(exp)
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)
        shake = 10  # Rung màn hình khi nổ

    # Va chạm tàu với thiên thạch (mask để chính xác hơn)
    ship_mask = pygame.mask.from_surface(ship.image)
    for asteroid in asteroids:
        offset = (asteroid.rect.left - ship.rect.left, asteroid.rect.top - ship.rect.top)
        if ship_mask.overlap(pygame.mask.from_surface(asteroid.image), offset):
            pygame.mixer.music.stop()
            gameover_text = font.render("GAME OVER - Press any key to restart", True, (255, 0, 0))
            screen.blit(gameover_text, (WIDTH // 2 - 200, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(1000)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        # Reset game
                        score = 0
                        all_sprites.empty()
                        missiles.empty()
                        asteroids.empty()
                        explosions.empty()
                        ship = Ship(WIDTH // 2, HEIGHT // 2)
                        all_sprites.add(ship)
                        for _ in range(3):
                            asteroid = Asteroid()
                            all_sprites.add(asteroid)
                            asteroids.add(asteroid)
                        pygame.mixer.music.play(-1)
                        waiting = False

    # Sinh thêm thiên thạch theo thời gian (chỉ khi số lượng nhỏ hơn 6)
    now = pygame.time.get_ticks()
    if now - last_spawn_time > SPAWN_INTERVAL and len(asteroids) < 6:
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)
        last_spawn_time = now

    # Rung màn hình
    offset_x = random.randint(-shake, shake) if shake > 0 else 0
    offset_y = random.randint(-shake, shake) if shake > 0 else 0
    shake = max(shake - 1, 0)

    # Vẽ nền và sprite với rung
    screen.blit(background, (offset_x, offset_y))
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect.move(offset_x, offset_y))

    # Hiển thị điểm
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)