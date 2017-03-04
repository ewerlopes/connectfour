from objects import *
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

        self.board_cell_image = utils.load_image('board_cell.png')

        logging.info('Loading sounds')

        self.placed_sound = utils.load_sound('placed.wav')
        self.column_change_sound = utils.load_sound('column_change.wav')

        logging.info('Loading fonts')

        self.title_font = utils.load_font('monofur.ttf', 36)

        self.chips = pygame.sprite.Group()

        self.player_controlled_chip = None

    def draw_board(self):
        self.window.blit(self.title_font.render('Red player turn', True, config.COLORS['white']), (10, 10))

        for x in range(0, config.COLS):
            for y in range(0, config.ROWS):
                self.window.blit(self.board_cell_image, (x * config.IMAGES_SIDE_SIZE, y * config.IMAGES_SIDE_SIZE + config.BOARD_MARGIN_TOP))

    def choose_column(self):
        if not self.player_controlled_chip:
            self.player_controlled_chip = RedChip()

            self.chips.add(self.player_controlled_chip)
            self.player_controlled_chip.rect.left = 0
            self.player_controlled_chip.rect.top = config.COLUMN_CHOOSING_MARGIN_TOP

        for event in pygame.event.get():
            utils.try_quit(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.player_controlled_chip.rect.left - config.IMAGES_SIDE_SIZE >= 0:
                    self.column_change_sound.play()
                    self.player_controlled_chip.rect.left -= config.IMAGES_SIDE_SIZE
                elif event.key == pygame.K_RIGHT and self.player_controlled_chip.rect.right + config.IMAGES_SIDE_SIZE <= config.WINDOW_SIZE[0]:
                    self.column_change_sound.play()
                    self.player_controlled_chip.rect.right += config.IMAGES_SIDE_SIZE
                elif event.key == pygame.K_DOWN:
                    self.status = 'CHIP_FALLS'

        self.chips.draw(self.window)

    def make_chip_fall(self):
        for event in pygame.event.get():
            utils.try_quit(event)

        if self.player_controlled_chip.rect.bottom + 5 <= config.WINDOW_SIZE[1]:
            self.player_controlled_chip.rect.bottom += 5
        else:
            self.placed_sound.play()
            self.player_controlled_chip.rect.bottom = config.WINDOW_SIZE[1]
            self.status = 'CHOOSING_COLUMN'
            self.player_controlled_chip = None

        self.chips.draw(self.window)

    def play(self):
        self.window.fill(config.COLORS['black'])

        if self.status == 'CHOOSING_COLUMN':
            self.choose_column()
        elif self.status == 'CHIP_FALLS':
            self.make_chip_fall()

        self.draw_board()

        pygame.display.update()

        self.clock.tick(config.FPS)
