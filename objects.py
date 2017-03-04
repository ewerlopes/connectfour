import pygame
import utils


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
