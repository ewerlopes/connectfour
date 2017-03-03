import pygame
import config
import utils


class Game:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

        self.board_cell = utils.load_image('board_cell.png')
        self.red_chip = utils.load_image('red_chip.png')
        self.red_chip_rect = self.red_chip.get_rect()

    def play(self):
        for event in pygame.event.get():
            utils.try_quit(event)

        self.window.fill(config.COLORS['black'])

        if self.red_chip_rect.bottom < config.WINDOW_SIZE[1]:
            self.red_chip_rect = self.red_chip_rect.move((0, 15))

        self.window.blit(self.red_chip, self.red_chip_rect)

        for x in range(0, config.COLS):
            for y in range(0, config.ROWS):
                self.window.blit(self.board_cell, (x * config.IMAGES_SIDE_SIZE, y * config.IMAGES_SIDE_SIZE))

        pygame.display.update()

        self.clock.tick(config.FPS)
