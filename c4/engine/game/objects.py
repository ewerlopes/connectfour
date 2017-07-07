from abc import ABCMeta, abstractmethod

import pygame
import settings
import utils

"""
This class has classes for the game objects: Chips and Players.
"""

class RedChip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = utils.load_image('red_chip.png')
        self.rect = self.image.get_rect()


class YellowChip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = utils.load_image('yellow_chip.png')
        self.rect = self.image.get_rect()


class Player:
    __metaclass__ = ABCMeta

    def __init__(self, engine, chip, color, name, id, score):
        self.engine = engine
        self.chip = chip
        self.color = color
        self.name = name
        self.id = id
        self.score = score


class RedPlayer(Player):
    def __init__(self, engine):
        Player.__init__ (self, engine, RedChip, settings.COLORS.RED.value, 'Red', 'RED', 0)


class YellowPlayer(Player):
    def __init__(self, engine):
        Player.__init__(self, engine, YellowChip, settings.COLORS.YELLOW.value, 'Yellow', 'YELLOW', 0)
