from objects import *
import pygame
import config
import utils


class Game:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

        self.window.fill((0, 0, 0))

        self.board_cell = utils.load_image('board_cell.png')

    def play(self):
        for event in pygame.event.get():
            utils.try_quit(event)

        chips = pygame.sprite.Group()

        red_chip = RedChip()
        red_chip.add(chips)
        chips.draw(self.window)

        for x in range(0, config.COLS):
            for y in range(0, config.ROWS):
                self.window.blit(self.board_cell, (x * config.IMAGES_SIDE_SIZE, y * config.IMAGES_SIDE_SIZE))

        pygame.display.update()

        self.clock.tick(config.FPS)
