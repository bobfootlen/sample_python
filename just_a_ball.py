import pygame
import sys
import math
import random

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))


# Initialize PyGame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Bouncer 3000")

# Set up clock
clock = pygame.time.Clock()
FPS = 60

# Ball class
class Ball:
    def __init__(self, x, y, radius=20, color=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color or self.random_color()
        self.vx = random.choice([-4, -3, 3, 4])
        self.vy = random.choice([-4, -3, 3, 4])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        wall_bounce = False
        # Wall bounce
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.vx *= -1
            self.x = clamp(self.x, 0 + self.radius, WIDTH - self.radius)
            wall_bounce = True
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.vy *= -1
            self.y = clamp(self.y, 0 + self.radius, HEIGHT - self.radius)
            wall_bounce = True
        return wall_bounce

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def collides_with(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        return distance < self.radius + other.radius
    
    def reverse(self):
            self.vy *= -1
            self.vx *= -1
    
    def resolve_collision(b1, b2):
        dx = b1.x - b2.x
        dy = b1.y - b2.y
        dist_sq = dx * dx + dy * dy
        if dist_sq == 0:
            return  # avoid divide-by-zero

        # Relative velocity
        dvx = b1.vx - b2.vx
        dvy = b1.vy - b2.vy

        # Dot product of velocity diff and position diff
        dot = dvx * dx + dvy * dy
        if dot > 0:
            return  # they’re moving apart

        # Scale factor
        scale = dot / dist_sq

        # Apply impulse
        b1.vx -= dx * scale
        b1.vy -= dy * scale
        b2.vx += dx * scale
        b2.vy += dy * scale


    @staticmethod
    def random_color():
        return random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)

balls = []

balls.append(Ball(WIDTH // 2, HEIGHT // 2, 50))

score = 0
# Main loop
running = True
while running:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            new_ball = Ball(mx, my)

            if all(not new_ball.collides_with(b) for b in balls):
                balls.append(new_ball)
                
    screen.fill((0, 0, 0))  # Black background

    for ball in balls:
        if ball.update():
            score += 1
        ball.draw(screen)
        
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            b1 = balls[i]
            b2 = balls[j]
            if abs(b1.x - b2.x) > b1.radius + b2.radius: continue
            if abs(b1.y - b2.y) > b1.radius + b2.radius: continue
            if b1.collides_with(b2):
                b1.resolve_collision(b2)
        
    # Draw everything
    pygame.display.flip()
    
    pygame.display.set_caption(f"Idle Bouncer 3000 score: {score} fps: {clock.get_fps():.2f}")

# Quit
pygame.quit()
sys.exit()
