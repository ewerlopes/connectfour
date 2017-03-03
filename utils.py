import pygame
import sys
import os


def try_quit(event):
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()


def _get_resource_path(res_type, filename):
    path = os.path.join('resources', res_type, filename)

    if not os.path.isfile(path):
        raise ValueError('The file ' + path + ' doesn\'t exist')

    return path


def load_image(filename):
    path = _get_resource_path('images', filename)

    return pygame.image.load(path).convert_alpha()


def load_sound(filename):
    path = _get_resource_path('sounds', filename)

    return pygame.mixer.Sound(file=path)


def load_font(filename, size):
    path = _get_resource_path('fonts', filename)

    return pygame.font.Font(path, size)
