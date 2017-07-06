import pygame
import utils
import settings
from abc import ABCMeta, abstractmethod

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

    def __init__(self, chip, color, name, id, score):
        self.chip = chip
        self.color = color
        self.name = name
        self.id = id
        self.score = score

    @abstractmethod
    def move(self, state, game_problem):
        """
        Defines the action to take. Return None in case the player is a human (allows for receive input).
        :return:
        """
        pass


class RedPlayer(Player):
    def __init__(self):
        Player.__init__(self,RedChip,settings.COLORS.RED.value,'Red','RED',0)

    def move(self, state, game_problem):
        pass

class YellowPlayer(Player):
    def __init__(self):
        Player.__init__(self, YellowChip, settings.COLORS.YELLOW.value, 'Yellow', 'YELLOW', 0)

    def move(self, state, game_problem):
        pass
