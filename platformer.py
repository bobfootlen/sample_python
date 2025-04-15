import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAVITY = 0.5
JUMP_STRENGTH = -12
SPEED = 10
ENEMY_SPEED = 4

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

# Player setup
player = pygame.Rect(100, 500, 40, 40)
velocity_y = 0
on_ground = False

# Platforms
platforms = [pygame.Rect(50, 550, 700, 20), pygame.Rect(300, 400, 150, 20), pygame.Rect(550, 300, 150, 20)]

# Enemies
enemies = [pygame.Rect(random.randint(100, 700), 500, 40, 40)]
enemy_direction = [1]  # 1 means right, -1 means left

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= SPEED
    if keys[pygame.K_d]:
        player.x += SPEED
    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = JUMP_STRENGTH
        on_ground = False
    
    # Apply gravity
    velocity_y += GRAVITY
    player.y += velocity_y
    
    # Collision detection
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform) and velocity_y > 0:
            player.y = platform.y - player.height
            velocity_y = 0
            on_ground = True
    
    # Move enemies
    for i, enemy in enumerate(enemies):
        enemy.x += ENEMY_SPEED * enemy_direction[i]
        if enemy.x <= 50 or enemy.x >= WIDTH - 50:
            enemy_direction[i] *= -1  # Reverse direction when hitting bounds
    
    # Check for enemy collision
    for enemy in enemies:
        if player.colliderect(enemy):
            print("Game Over!")
            running = False
    
    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)
    
    # Draw player
    pygame.draw.rect(screen, BLUE, player)
    
    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
