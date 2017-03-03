import pygame
import sys


def try_quit(event):
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()
