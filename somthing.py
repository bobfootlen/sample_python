import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ray Casting Example")

# Player properties
player_x = 100
player_y = 100
player_angle = 0
player_speed = 5

# Map definition (1 = wall, 0 = empty space)
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 1, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 1, 1, 0, 1, 0],
    [1, 0, 0, 1, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 0]
]

map_size = len(game_map)
tile_size = 64

# Ray casting properties
fov = math.pi / 3  # Field of view
num_rays = 120
max_depth = 500

# Functions
def draw_map():
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, (255, 255, 255), (x * tile_size, y * tile_size, tile_size, tile_size))

def cast_rays():
  for i in range(num_rays):
    ray_angle = player_angle - fov / 2 + (i / num_rays) * fov
    
    for depth in range(max_depth):
      target_x = player_x + depth * math.cos(ray_angle)
      target_y = player_y + depth * math.sin(ray_angle)
      
      map_x = int(target_x / tile_size)
      map_y = int(target_y / tile_size)
      
      if 0 <= map_x < map_size and 0 <= map_y < map_size and game_map[map_y][map_x] == 1:
        # Draw the ray
        pygame.draw.line(screen, (255, 0, 0), (player_x, player_y), (target_x, target_y))
        break
      elif depth == max_depth - 1:
          pygame.draw.line(screen, (255, 0, 0), (player_x, player_y), (target_x, target_y))

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_angle -= 0.1
            elif event.key == pygame.K_RIGHT:
                player_angle += 0.1
            elif event.key == pygame.K_UP:
                player_x += player_speed * math.cos(player_angle)
                player_y += player_speed * math.sin(player_angle)
            elif event.key == pygame.K_DOWN:
                player_x -= player_speed * math.cos(player_angle)
                player_y -= player_speed * math.sin(player_angle)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the map
    draw_map()

    # Cast rays
    cast_rays()

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()