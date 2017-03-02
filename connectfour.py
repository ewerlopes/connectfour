from objects import *
import pygame
import os

IMAGES_SIDE_SIZE = 112

COLS = 7
ROWS = 6


class ConnectFour:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Connect Four')

        self.window_width = IMAGES_SIDE_SIZE * COLS
        self.window_height = IMAGES_SIDE_SIZE * ROWS

        self.board = {}

        for x in range(0, COLS):
            self.board[x] = {}

            for y in range(0, ROWS):
                self.board[x][y] = None

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.screen.fill((0, 0, 0))

        self.clock = pygame.time.Clock()

    def draw_board(self):
        board_cell = pygame.image.load(os.path.join('images', 'board_cell.png')).convert_alpha()

        for x in range(0, COLS):
            for y in range(0, ROWS):
                self.screen.blit(board_cell, (x * IMAGES_SIDE_SIZE, y * IMAGES_SIDE_SIZE))

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
