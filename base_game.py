#was sprite_move
import pygame
import socket
import threading

players = {}
players_lock = threading.Lock()

def add_or_update_player(remote_addr, state):
    with players_lock:
        players[remote_addr] = state

pygame.init()

client_mode = False

remote = input("sever address")
face = ("none")

PORT = 5000

client = None
sever = None

if remote:
    client_mode = True
    HOST = remote  # Change to host's IP address
    client_name = input("username ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("Connected.")
    #client connect code
else:
    client_mode = False
    HOST = ''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print("Waiting for connection...")
    server.accept()
    #sever startup code

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

# Sprite starting position
x = 40
y = 0

#player position
player_x = 200
player_y = 200
speed = 5

# Game loop
run = True
clock = pygame.time.Clock()

def handle_speed_input(keys,speed):
    if keys[pygame.K_1]:
        speed = 1
    if keys[pygame.K_5]:
        speed = 5
    if keys[pygame.K_0]:
        speed = 20
    return speed

def handle_facing(face, screen, sprite_up, sprite_down, sprite_left, sprite_right, player_x, player_y):
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

def handle_walls(x, y):
    if (x) > (200):
        x = 200
    if (x) < (-9700):
        x = -9700
    if (y) > (200):
        y = 200
    if (y) < (-9700):
        y = -9700
    return x,y

def key_inputs(speed,x,y,face):
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
    return face,x,y,keys

while run:
    # Limit to 60 FPS
    clock.tick(60)  
    screen.fill(BG)

    # Key input
    face, x, y, keys = key_inputs(speed,x,y,face)

#draws the backround
    screen.blit(backround_sheet_image, (x, y))
    screen.blit(tree_1, (x + 300, y + 300))
    screen.blit(tree_2, (x + 100, y + 100))


#changes which way P1 is facing
    handle_facing(face, screen, sprite_up, sprite_down, sprite_left, sprite_right, player_x, player_y)
    

#lets you control your speed
    speed = handle_speed_input(keys,speed)

#this controls the wall
    x, y = handle_walls(x, y)


   # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#caption
    pygame.display.set_caption(f"python game: {x} {y} fps: {clock.get_fps():.2f}")

    pygame.display.update()

pygame.quit()