from objects import *
import pygame
import os
import logging
import sys

IMAGES_SIDE_SIZE = 112

COLS = 7
ROWS = 6


class ConnectFour:
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
            stream=sys.stdout
        )

        logging.getLogger().setLevel(logging.INFO)

        logging.info('Initializing PyGame {} (SDL {})'.format(
            pygame.version.ver,
            '.'.join(str(v) for v in pygame.get_sdl_version())
        ))

        pygame.init()

        self.width = IMAGES_SIDE_SIZE * COLS
        self.height = IMAGES_SIDE_SIZE * ROWS

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))

        logging.info('Loading images')

        self.images = {}

        self.images['board_cell'] = pygame.image.load(os.path.join('images', 'board_cell.png')).convert_alpha()

        logging.info('Initializing main window')

        pygame.display.set_caption('Connect Four')
        pygame.display.set_icon(pygame.image.load(os.path.join('images', 'icon.png')).convert_alpha())

        self.clock = pygame.time.Clock()

        logging.info('Initializing board model')

        self.board = {}

        for x in range(0, COLS):
            self.board[x] = {}

            for y in range(0, ROWS):
                self.board[x][y] = None

    def draw_board(self):
        for x in range(0, COLS):
            for y in range(0, ROWS):
                self.screen.blit(self.images['board_cell'], (x * IMAGES_SIDE_SIZE, y * IMAGES_SIDE_SIZE))

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            chips = pygame.sprite.Group()

            caca = RedChip()
            caca.add(chips)
            chips.draw(self.screen)

            self.draw_board()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    ConnectFour().run()
