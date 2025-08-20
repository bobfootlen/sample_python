import pygame
import random

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BASKET_WIDTH, BASKET_HEIGHT = 100, 20
APPLE_RADIUS = 15
SPEED = 10

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Apples")

# Load assets
basket = pygame.Rect(WIDTH // 2, HEIGHT - 50, BASKET_WIDTH, BASKET_HEIGHT)
apple = pygame.Rect(random.randint(0, WIDTH - APPLE_RADIUS * 2), 0, APPLE_RADIUS * 2, APPLE_RADIUS * 2)
score = 0
running = True
clock = pygame.time.Clock()

# Game loop
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move basket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket.x > 0:
        basket.x -= SPEED
    if keys[pygame.K_RIGHT] and basket.x < WIDTH - BASKET_WIDTH:
        basket.x += SPEED
    
    # Move apple
    apple.y += SPEED
    
    # Check collision
    if basket.colliderect(apple):
        score += 1
        apple.x = random.randint(0, WIDTH - APPLE_RADIUS * 2)
        apple.y = 0
    
    # Reset apple if it falls past the screen
    if apple.y > HEIGHT:
        apple.x = random.randint(0, WIDTH - APPLE_RADIUS * 2)
        apple.y = 0
    
    # Draw elements
    pygame.draw.rect(screen, GREEN, basket)
    pygame.draw.ellipse(screen, RED, apple)
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
