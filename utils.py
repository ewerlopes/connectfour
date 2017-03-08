from random import choice
import pygame
import os
import config


def _get_resource_path(res_type, filename):
    path = os.path.join(config.RESOURCES_ROOT, res_type, filename)

    if not os.path.isfile(path):
        raise ValueError('The file ' + path + ' doesn\'t exist')

    return path


def load_image(filename):
    path = _get_resource_path('images', filename)

    return pygame.image.load(path).convert_alpha()


def load_sound(filename):
    path = _get_resource_path('sounds', filename)

    sound = pygame.mixer.Sound(file=path)
    sound.set_volume(config.SOUNDS_VOLUME)

    return sound


def load_music(filename, play=True):
    path = _get_resource_path('musics', filename)

    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(config.MUSIC_VOLUME)

    if play:
        pygame.mixer.music.play(-1)


def load_random_music(filenames, play=True):
    load_music(choice(filenames), play)


def load_font(filename, size):
    path = _get_resource_path('fonts', filename)

    return pygame.font.Font(path, size)
