import pygame
import random

# Initialize pygame
pygame.init()

# Screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Shooter")

# Load and scale images
player_image = pygame.image.load("player.png").convert_alpha()  # Ensure the image is transparent
player_image = pygame.transform.scale(player_image, (64, 64))   # Resize to appropriate dimensions

bullet_image = pygame.image.load("bullet.png").convert_alpha()  # Ensure bullet transparency
bullet_image = pygame.transform.scale(bullet_image, (16, 16))   # Resize bullet

alien_image = pygame.image.load("alien.png").convert_alpha()    # Alien image
alien_image = pygame.transform.scale(alien_image, (50, 50))     # Scale alien to match player

background_image = pygame.image.load("space_background.jpg").convert()  # Background image

# Sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.mp3")

# **Background Music**
pygame.mixer.music.load("background_music.mp3")  # Replace with the actual music file
pygame.mixer.music.play(-1)  # Loop indefinitely

# Font for text
font = pygame.font.Font(None, 36)

# Game classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 8
        self.health = 3

    def update(self, keys=None):
        if keys:
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = alien_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            spawn_alien()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Helper function to spawn aliens
def spawn_alien():
    alien = Alien()
    all_sprites.add(alien)
    aliens.add(alien)

# Sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Player instance
player = Player()
all_sprites.add(player)

# Spawn initial aliens
for _ in range(5):
    spawn_alien()

# Game variables
score = 0
level = 1
running = True
clock = pygame.time.Clock()
alien_spawn_timer = 0

# Main game loop
while running:
    clock.tick(FPS)

    # Clear screen and redraw background
    screen.blit(background_image, (0, 0))

    # Event handling
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update all sprites
    player.update(keys)
    all_sprites.update()

    # Spawn aliens at intervals
    alien_spawn_timer += 1
    if alien_spawn_timer >= 90:
        spawn_alien()
        alien_spawn_timer = 0

    # Check collisions
    for bullet in bullets:
        collided_aliens = pygame.sprite.spritecollide(bullet, aliens, True)
        if collided_aliens:
            bullet.kill()
            score += 10
            explosion_sound.play()
            spawn_alien()

    # Player collision with aliens
    collided_aliens = pygame.sprite.spritecollide(player, aliens, True)
    if collided_aliens:
        player.health -= 1
        explosion_sound.play()
        if player.health <= 0:
            running = False
        for alien in collided_aliens:
            alien.kill()
            spawn_alien()

    # Draw everything
    all_sprites.draw(screen)

    # Display text
    score_text = font.render(f"Score: {score}", True, GREEN)
    health_text = font.render(f"Health: {player.health}", True, RED)
    level_text = font.render(f"Level: {level}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (SCREEN_WIDTH - 150, 10))
    screen.blit(level_text, (SCREEN_WIDTH - 150, 40))

    # Level up logic
    if score >= level * 100:
        level += 1
        for alien in aliens:
            alien.speed += 1

    pygame.display.flip()

# Stop background music when game ends
pygame.mixer.music.stop()

pygame.quit()
