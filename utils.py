import pygame
import sys
import os


def try_quit(event):
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()


def load_image(filename):
    path = os.path.join('resources', 'images', filename)

    if not os.path.isfile(path):
        raise ValueError('The image ' + path + ' doesn\'t exist')

    return pygame.image.load(path).convert_alpha()
