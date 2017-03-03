import pygame
import config
import utils
import logging


class Game:
    status = 'CHOOSING_COLUMN'

    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

        logging.info('Loading images')

        self.board_cell = utils.load_image('board_cell.png')
        self.red_chip = utils.load_image('red_chip.png')
        self.yellow_chip = utils.load_image('yellow_chip.png')

        logging.info('Loading sounds')

        self.placed = utils.load_sound('placed.wav')
        self.placed.set_volume(config.SOUNDS_VOLUME)

        self.column_change = utils.load_sound('column_change.wav')
        self.column_change.set_volume(config.SOUNDS_VOLUME)

        self.player_controlled_chip = None
        self.player_controlled_chip_rect = None

    def draw_board(self):
        for x in range(0, config.COLS):
            for y in range(0, config.ROWS):
                self.window.blit(self.board_cell, (x * config.IMAGES_SIDE_SIZE, y * config.IMAGES_SIDE_SIZE + config.BOARD_MARGIN_TOP))

    def choose_column(self):
        if not self.player_controlled_chip:
            self.player_controlled_chip = self.red_chip
            self.player_controlled_chip_rect = self.player_controlled_chip.get_rect()
            self.player_controlled_chip_rect.x = 0
            self.player_controlled_chip_rect.y = config.COLUMN_CHOOSING_MARGIN_TOP

        for event in pygame.event.get():
            utils.try_quit(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.player_controlled_chip_rect.x - config.IMAGES_SIDE_SIZE >= 0:
                    self.column_change.play()
                    self.player_controlled_chip_rect.x -= config.IMAGES_SIDE_SIZE
                elif event.key == pygame.K_RIGHT and self.player_controlled_chip_rect.x + config.IMAGES_SIDE_SIZE <= config.WINDOW_SIZE[0] - config.IMAGES_SIDE_SIZE:
                    self.column_change.play()
                    self.player_controlled_chip_rect.x += config.IMAGES_SIDE_SIZE

        self.window.blit(self.player_controlled_chip, self.player_controlled_chip_rect)

    def play(self):
        self.window.fill(config.COLORS['black'])

        if self.status == 'CHOOSING_COLUMN':
            self.choose_column()
        elif self.status == 'CHIP_FALLS':
            pass

        self.draw_board()

        pygame.display.update()

        self.clock.tick(config.FPS)
