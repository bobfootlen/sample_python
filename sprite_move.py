#note this is chatgpt code

import pygame

pygame.init()

face = ("none")

# Screen setup
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('sprite move')

# Load sprite
sprite_up = pygame.image.load('img/up.png').convert_alpha()
sprite_down = pygame.image.load('img/down.png').convert_alpha()
sprite_left = pygame.image.load('img/left.png').convert_alpha()
sprite_right = pygame.image.load('img/right.png').convert_alpha()

backround_sheet_image = pygame.image.load('img/backround1.png').convert_alpha()

# Background color
BG = (50, 50, 50)

# Sprite position
x = 150
y = 150
speed = 6

# Game loop
run = True
clock = pygame.time.Clock()

while run:
    clock.tick(60)  # Limit to 60 FPS
    screen.fill(BG)

    # Key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x -= speed
        face = ("left")
    if keys[pygame.K_d]:
        x += speed
        face = ("right")
    if keys[pygame.K_w]:
        y -= speed
        face = ("uper")
    if keys[pygame.K_s]:
        y += speed
        face = ("down")


    screen.blit(backround_sheet_image, (0, 0))

    if face == ("uper") :
        screen.blit(sprite_up, (x, y))
    if face == ("down") :
        screen.blit(sprite_down, (x, y))
    if face == ("right") :
        screen.blit(sprite_right, (x, y))
    if face == ("left") :
        screen.blit(sprite_left, (x, y))
    if face == ("none") :
        screen.blit(sprite_up, (x, y))
    
    
    # Draw the sprite at the new position
    #screen.blit(sprite_up, (x, y))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()