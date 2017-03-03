import pygame
import utils

__all__ = [
    'RedChip',
    'YellowChip'
]


class Chip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()


class RedChip(Chip):
    def __init__(self):
        self.image = utils.load_image('red_chip.png')

        Chip.__init__(self)


class YellowChip(Chip):
    def __init__(self):
        self.image = utils.load_image('yellow_chip.png')

        Chip.__init__(self)
