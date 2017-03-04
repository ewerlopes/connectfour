import objects
import pygame
import config
import utils
import logging


class Game:
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

        logging.info('Initializing game')

        self.chips = pygame.sprite.Group()
        self.current_player_chip = None
        self.current_player = objects.RedPlayer()
        self.current_player_chip_column = 0

        self.board = {}

        for x in range(0, config.COLS):
            self.board[x] = {}

            for y in range(0, config.ROWS):
                self.board[x][y] = None

    def draw_player_turn(self):
        text = self.title_font.render(self.current_player.name + ' player turn', True, self.current_player.color)
        text_rect = text.get_rect()
        text_rect.centerx = config.WINDOW_SIZE[0] / 2
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
                if event.key == pygame.K_LEFT and self.current_player_chip.rect.left - config.IMAGES_SIDE_SIZE >= 0:
                    self.column_change_sound.play()
                    self.current_player_chip.rect.left -= config.IMAGES_SIDE_SIZE
                    self.current_player_chip_column -= 1
                elif event.key == pygame.K_RIGHT and self.current_player_chip.rect.right + config.IMAGES_SIDE_SIZE <= config.WINDOW_SIZE[0]:
                    self.column_change_sound.play()
                    self.current_player_chip.rect.right += config.IMAGES_SIDE_SIZE
                    self.current_player_chip_column += 1
                elif event.key == pygame.K_DOWN:
                    self.placed_sound.play()
                    self.current_player_chip.rect.bottom = config.WINDOW_SIZE[1]
                    self.current_player_chip = None
                    self.current_player = objects.YellowPlayer() if self.current_player.name == 'Red' else objects.RedPlayer()
                    self.current_player_chip_column = 0

        self.chips.draw(self.window)

        self.draw_player_turn()
        self.draw_board()

        pygame.display.update()

        self.clock.tick(config.FPS)
