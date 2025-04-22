#note this is chatgpt code

import pygame

pygame.init()

# Screen setup
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500  # Fixed the typo from HIGHT to HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('sprite test 01')

# Load sprite
sprite_sheet_image = pygame.image.load('spriteP1.png').convert_alpha()

# Background color
BG = (200, 200, 200)

# Sprite position
x = 150
y = 150
speed = 10

# Game loop
run = True
clock = pygame.time.Clock()

while run:
    clock.tick(60)  # Limit to 60 FPS
    screen.fill(BG)

    # Key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # Draw the sprite at the new position
    screen.blit(sprite_sheet_image, (x, y))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()