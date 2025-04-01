import pygame
import sys

# Initialize PyGame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Bouncer 3000")

# Set up clock
clock = pygame.time.Clock()
FPS = 60

# Ball properties
ball_radius = 50
ball_x = WIDTH // 2 # Start in Center
ball_y = HEIGHT // 2
ball_speed_x = 5 # Start with 5/4 slope
ball_speed_y = 4
ball_color = (100, 100, 255)  # a non-Red color
score = 0
# Main loop
running = True
while running:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Bounce off walls
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_speed_x *= -1
        score += 1
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_speed_y *= -1
        score += 1

    # Draw everything
    screen.fill((0, 0, 0))  # Black background
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)
    pygame.display.flip()
    
    pygame.display.set_caption("Idle Bouncer 3000 score: " + str(score))

# Quit
pygame.quit()
sys.exit()
