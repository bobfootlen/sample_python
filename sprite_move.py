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

#trees
tree_1 = pygame.image.load('img/tree-1.png').convert_alpha()
tree_2 = pygame.image.load('img/tree-2.png').convert_alpha()

#loads the backround.png
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
    # Limit to 60 FPS
    clock.tick(60)  
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

#draws the backround
    screen.blit(backround_sheet_image, (x, y))
    screen.blit(tree_1, (x + 300, y + 300))
    screen.blit(tree_2, (x + 100, y + 100))


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
    

#lets you control your speed
    if keys[pygame.K_1]:
        speed = 1
    if keys[pygame.K_5]:
        speed = 5
    if keys[pygame.K_0]:
        speed = 10

#this controls the wall
    if (x) > (200):
        x = 200
    if (x) < (-9700):
        x = -9700
    if (y) > (200):
        y = 200
    if (y) < (-9700):
        y = -9700


   # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#caption
    pygame.display.set_caption(f"python game: {x} {y} fps: {clock.get_fps():.2f}")

    pygame.display.update()

pygame.quit()