import objects
import pygame
import config
import utils
import logging
from pprint import pprint


class Game:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

        logging.info('Loading images')

        self.board_cell_image = utils.load_image('board_cell.png')

        logging.info('Loading sounds')

        self.placed_sound = utils.load_sound('placed.wav')
        self.column_change_sound = utils.load_sound('column_change.wav')
        self.column_full_sound = utils.load_sound('column_full.wav')

        logging.info('Loading the music')

        utils.load_music('bg_music.wav')

        logging.info('Loading fonts')

        self.title_font = utils.load_font('monofur.ttf', 36)
        self.normal_font = utils.load_font('monofur.ttf', 18)

        logging.info('Initializing game')

        self.chips = pygame.sprite.Group()
        self.red_player = objects.RedPlayer()
        self.yellow_player = objects.YellowPlayer()
        self.current_player = self.red_player # The starting player is always the red one
        self.current_player_chip = None
        self.current_player_chip_column = 0

        self.board = {}

        for x in range(0, config.COLS):
            self.board[x] = {}

            for y in range(0, config.ROWS):
                self.board[x][y] = None

    def draw_game_name(self):
        text = self.normal_font.render('Connect Four ' + config.__version__, True, config.COLORS.WHITE.value)
        text_rect = text.get_rect()
        text_rect.y = 10
        text_rect.right = self.window.get_rect().width - 10

        self.window.blit(text, text_rect)

    def draw_player_turn(self):
        text = self.title_font.render(self.current_player.name + ' player turn', True, self.current_player.color)
        text_rect = text.get_rect()
        text_rect.centerx = self.window.get_rect().centerx
        text_rect.y = 10

        self.window.blit(text, text_rect)

    def draw_board(self):
        for x in range(0, config.COLS):
            for y in range(0, config.ROWS):
                self.window.blit(self.board_cell_image, (x * config.IMAGES_SIDE_SIZE, y * config.IMAGES_SIDE_SIZE + config.BOARD_MARGIN_TOP))

    def play(self):
        self.window.fill(config.COLORS.BLACK.value)

        if not self.current_player_chip:
            self.current_player_chip = self.current_player.chip()

            self.chips.add(self.current_player_chip)
            self.current_player_chip.rect.left = 0
            self.current_player_chip.rect.top = config.COLUMN_CHOOSING_MARGIN_TOP

        for event in pygame.event.get():
            utils.try_quit(event)

            if event.type == pygame.KEYDOWN:
                # Move chip to the left: before, make sure we'll not go beyond the screen limits
                if event.key == pygame.K_LEFT and self.current_player_chip.rect.left - config.IMAGES_SIDE_SIZE >= 0:
                    self.column_change_sound.play()
                    self.current_player_chip.rect.left -= config.IMAGES_SIDE_SIZE
                    self.current_player_chip_column -= 1
                # Move chip to the right: before, make sure we'll not go beyond the screen limits
                elif event.key == pygame.K_RIGHT and self.current_player_chip.rect.right + config.IMAGES_SIDE_SIZE <= config.WINDOW_SIZE[0]:
                    self.column_change_sound.play()
                    self.current_player_chip.rect.right += config.IMAGES_SIDE_SIZE
                    self.current_player_chip_column += 1
                # Drop the chip in the current column
                elif event.key == pygame.K_DOWN:
                    chip_row_stop = None

                    # Check all rows in the currently selected column starting from the top
                    for y, cell in self.board[self.current_player_chip_column].items():
                        # If there's nothing in the current cell
                        if not cell:
                            # If we're in the latest cell or if the next cell isn't empty
                            if (y == config.ROWS - 1) or (not y + 1 > config.ROWS - 1 and self.board[self.current_player_chip_column][y + 1]):
                                chip_row_stop = y + 1
                                self.board[self.current_player_chip_column][y] = self.current_player.name

                    # Actually move the chip in the current column and reset the current one (to create a new one later)
                    if chip_row_stop:
                        self.placed_sound.play()
                        self.current_player_chip.rect.top += config.IMAGES_SIDE_SIZE * chip_row_stop

                        self.current_player_chip = None
                        self.current_player_chip_column = 0

                        # It's the other player's turn
                        self.current_player = self.yellow_player if isinstance(self.current_player, objects.RedPlayer) else self.red_player
                    # The column is full
                    else:
                        self.column_full_sound.play()

        self.chips.draw(self.window)

        self.draw_player_turn()
        self.draw_game_name()
        self.draw_board()

        pygame.display.update()

        self.clock.tick(config.FPS)
