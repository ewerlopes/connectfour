import pygame
import os

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
        self.image = pygame.image.load(os.path.join('images', 'red_chip.png')).convert_alpha()

        Chip.__init__(self)


class YellowChip(Chip):
    def __init__(self):
        self.image = pygame.image.load(os.path.join('images', 'yellow_chip.png')).convert_alpha()

        Chip.__init__(self)
