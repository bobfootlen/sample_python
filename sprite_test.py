import pygame

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
pygame.display.set_caption('sprite test 01')

sprite_sheet_image = pygame.image.load('spriteP1.png').convert_alpha()

BG =(200, 200, 200)

run = True
while run:

    screen.fill(BG)

    screen.blit(sprite_sheet_image, (150, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.QUIT()

