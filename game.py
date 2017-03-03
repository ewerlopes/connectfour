from objects import *
import pygame
import config
import utils
import os


class Game:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

        self.window.fill((0, 0, 0))

    def play(self):
        for event in pygame.event.get():
            utils.try_quit(event)

        chips = pygame.sprite.Group()

        caca = RedChip()
        caca.add(chips)
        chips.draw(self.window)

        board_cell = pygame.image.load(os.path.join('images', 'board_cell.png')).convert_alpha()

        for x in range(0, config.COLS):
            for y in range(0, config.ROWS):
                self.window.blit(board_cell, (x * config.IMAGES_SIDE_SIZE, y * config.IMAGES_SIDE_SIZE))

        pygame.display.update()
        self.clock.tick(config.FPS)