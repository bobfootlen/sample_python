import pygame

pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kill Box Example")

# Define colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Player class (using pygame.sprite.Sprite)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def kill(self):
        print("Player died!")
        # Handle respawn or game over logic here
        self.rect.x = 100
        self.rect.y = 100

# Create player and kill box
player = Player(100, 100, 30, 30, blue)
kill_box = pygame.Rect(300, 400, 200, 50)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game elements
    player.update()

    # Check for collision with kill box
    if kill_box.colliderect(player.rect):
        player.kill()

    # Draw everything
    screen.fill(white)
    pygame.draw.rect(screen, red, kill_box)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()