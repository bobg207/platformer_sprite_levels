import pygame
import sprites
from settings import *

pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()
playing = True

layout = sprites.Layout()

while playing:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(WHITE)

    layout.update(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
