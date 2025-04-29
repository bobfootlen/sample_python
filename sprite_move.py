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
x = 0
y = 0

#player position
player_x = 200
player_y = 200
speed = 5

# Game loop
run = True
clock = pygame.time.Clock()

while run:
    clock.tick(60)  # Limit to 60 FPS
    screen.fill(BG)

    # Key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x += speed
        face = ("left")
    if keys[pygame.K_d]:
        x -= speed
        face = ("right")
    if keys[pygame.K_w]:
        y += speed
        face = ("up")
    if keys[pygame.K_s]:
        y -= speed
        face = ("down")

#draws th backround
    screen.blit(backround_sheet_image, (x, y))


#changes which way P1 is facing
    if face == ("up") :
        screen.blit(sprite_up, (player_x, player_y))
    if face == ("down") :
        screen.blit(sprite_down, (player_x, player_y))
    if face == ("right") :
        screen.blit(sprite_right, (player_x, player_y))
    if face == ("left") :
        screen.blit(sprite_left, (player_x, player_y))
    if face == ("none") :
        screen.blit(sprite_up, (player_x, player_y))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.set_caption(f"python game: {x} {y} fps: {clock.get_fps():.2f}")

    pygame.display.update()

pygame.quit()