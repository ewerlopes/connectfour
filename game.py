import objects
import pygame
import config
import utils
import logging


class Game:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

        self.chips = pygame.sprite.Group()
        self.red_player = objects.RedPlayer()
        self.yellow_player = objects.YellowPlayer()

        logging.info('Loading images')

        self.board_cell_image = utils.load_image('board_cell.png')

        logging.info('Loading sounds')

        self.placed_sound = utils.load_sound('placed.wav')
        self.column_change_sound = utils.load_sound('column_change.wav')
        self.column_full_sound = utils.load_sound('column_full.wav')
        self.win_sound = utils.load_sound('win.wav')
        self.applause_sound = utils.load_sound('applause.wav')
        self.boo_sound = utils.load_sound('boo.wav')

        logging.info('Loading fonts')

        self.title_font = utils.load_font('monofur.ttf', 22)
        self.normal_font = utils.load_font('monofur.ttf', 16)

        self.init_new_game()

    def init_new_game(self):
        logging.info('Starting new game')

        self.state = config.GAME_STATES.PLAYING

        self.chips.empty()

        self.current_player = self.red_player # The starting player is always the red one
        self.current_player_chip = None
        self.current_player_chip_column = 0

        self.board = {}

        for x in range(0, config.COLS):
            self.board[x] = {}

            for y in range(0, config.ROWS):
                self.board[x][y] = None

        logging.info('Loading random music')

        utils.load_random_music(['techno_dreaming.wav', 'techno_celebration.wav', 'electric_rain.wav', 'snake_trance.wav'])

    def draw_game_name(self):
        text = self.normal_font.render('Connect Four ' + config.VERSION, True, config.COLORS.WHITE.value)
        text_rect = text.get_rect()
        text_rect.y = 10
        text_rect.right = self.window.get_rect().width - 10

        self.window.blit(text, text_rect)

    def draw_title(self, title, color):
        text = self.title_font.render(title, True, color)
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.y = 10

        self.window.blit(text, text_rect)

    def is_valid_position(self, x, y):
        if x < 0 or x > config.COLS - 1 or y < 0 or y > config.ROWS - 1:
            return False

        return True

    def compute_direction_pos(self, x, y, direction):
        x = x + abs(direction[0]) if direction[0] > 0 else x - abs(direction[0])
        y = y + abs(direction[1]) if direction[1] > 0 else y - abs(direction[1])

        return x, y

    def count_consecutive_diagonal_chips(self, consecutive_chips, previous_chip, x, y, direction):
        if not self.is_valid_position(x, y):
            return consecutive_chips

        cell = self.board[x][y]

        if cell == self.current_player.name and consecutive_chips == 0:
            consecutive_chips = 1
        elif cell == self.current_player.name and cell == previous_chip:
            consecutive_chips += 1

        x, y = self.compute_direction_pos(x, y, direction)

        previous_chip = cell

        return self.count_consecutive_diagonal_chips(consecutive_chips, previous_chip, x, y, direction)

    def did_i_win(self):
        """Check if the current player win the game.

        This method performs the checks on the whole board in all possible direction until 4 consecutive chips are found
        for the current player.
        """

        # Check each columns from left to right
        for x in range(0, config.COLS):
            consecutive_chips = 0
            previous_chip = None

            for y in range(0, config.ROWS):
                cell = self.board[x][y]

                if cell == self.current_player.name and consecutive_chips == 0:
                    consecutive_chips = 1
                elif cell == self.current_player.name and cell == previous_chip:
                    consecutive_chips += 1

                if consecutive_chips == 4:
                    return True

                previous_chip = cell

        # Check each rows from top to bottom
        for y in range(0, config.ROWS):
            consecutive_chips = 0
            previous_chip = None

            for x in range(0, config.COLS):
                cell = self.board[x][y]

                if cell == self.current_player.name and consecutive_chips == 0:
                    consecutive_chips = 1
                elif cell == self.current_player.name and cell == previous_chip:
                    consecutive_chips += 1

                if consecutive_chips == 4:
                    return True

                previous_chip = cell

        # Check each "/" diagonal starting at the top left corner
        x = 0

        for y in range(0, config.ROWS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1))

            if consecutive_chips == 4:
                return True

        # Check each "/" diagonal starting at the bottom left + 1 corner
        y = config.ROWS - 1

        for x in range(1, config.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1))

            if consecutive_chips == 4:
                return True

        # Check each "\" diagonal starting at the bottom left corner
        x = 0

        for y in range(config.ROWS, -1, -1):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1))

            if consecutive_chips == 4:
                return True

        # Check each "\" diagonal starting at the top left + 1 corner
        y = 0

        for x in range(1, config.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1))

            if consecutive_chips == 4:
                return True

        return False

    def did_no_one_win(self):
        """Check if no one win the game.

        This method checks every single cell. If all are filled, no one win."""
        for x in range(0, config.COLS):
            for y in range(0, config.ROWS):
                if not self.board[x][y]: # The cell is empty: players still can play
                    return False

        return True

    def draw_board(self):
        """Draw the board itself (the game support)."""
        for x in range(0, config.COLS):
            for y in range(0, config.ROWS):
                self.window.blit(self.board_cell_image, (x * config.IMAGES_SIDE_SIZE, y * config.IMAGES_SIDE_SIZE + config.BOARD_MARGIN_TOP))

    def get_free_row(self, column):
        """Given a column, get the latest row number which is free."""
        for y, cell in self.board[column].items():
            # If there's nothing in the current cell
            if not cell:
                # If we're in the latest cell or if the next cell isn't empty
                if (y == config.ROWS - 1) or (not y + 1 > config.ROWS - 1 and self.board[column][y + 1]):
                    return y

        return False

    def draw_background(self):
        blue_rect = pygame.Rect((0, 0), (config.WINDOW_SIZE[0], config.BOARD_MARGIN_TOP))
        black_rect = pygame.Rect((0, config.BOARD_MARGIN_TOP), (config.WINDOW_SIZE[0], config.IMAGES_SIDE_SIZE * config.ROWS))

        self.window.fill(config.COLORS.BLUE.value, blue_rect)
        self.window.fill(config.COLORS.BLACK.value, black_rect)

    def play(self):
        self.draw_background()
        self.draw_game_name()

        if self.state == config.GAME_STATES.PLAYING:
            if not self.current_player_chip:
                self.current_player_chip = self.current_player.chip()

                self.chips.add(self.current_player_chip)
                self.current_player_chip.rect.left = 0
                self.current_player_chip.rect.top = config.COLUMN_CHOOSING_MARGIN_TOP

            for event in pygame.event.get():
                utils.try_quit(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: # Move chip to the left
                        self.column_change_sound.play()

                        if self.current_player_chip.rect.left - config.IMAGES_SIDE_SIZE >= 0: # The chip will not go beyond the screen
                            self.current_player_chip.rect.left -= config.IMAGES_SIDE_SIZE
                            self.current_player_chip_column -= 1
                        else: # The chip will go beyond the screen: put it in the far right
                            self.current_player_chip.rect.right = config.WINDOW_SIZE[0]
                            self.current_player_chip_column = config.COLS - 1
                    elif event.key == pygame.K_RIGHT: # Move chip to the right
                        self.column_change_sound.play()

                        if self.current_player_chip.rect.right + config.IMAGES_SIDE_SIZE <= config.WINDOW_SIZE[0]: # The chip will not go beyond the screen
                            self.current_player_chip.rect.right += config.IMAGES_SIDE_SIZE
                            self.current_player_chip_column += 1
                        else: # The chip will go beyond the screen: put it in the far left
                            self.current_player_chip.rect.left = 0
                            self.current_player_chip_column = 0
                    elif event.key == pygame.K_DOWN: # Drop the chip in the current column
                        # Check all rows in the currently selected column starting from the top
                        chip_row_stop = self.get_free_row(self.current_player_chip_column)

                        if chip_row_stop is not False: # Actually move the chip in the current column and reset the current one (to create a new one later)
                            self.placed_sound.play()
                            self.board[self.current_player_chip_column][chip_row_stop] = self.current_player.name
                            self.current_player_chip.rect.top += config.IMAGES_SIDE_SIZE * (chip_row_stop + 1)

                            if self.did_i_win():
                                pygame.mixer.music.stop()
                                self.win_sound.play()
                                self.applause_sound.play()
                                self.state = config.GAME_STATES.WON
                            elif self.did_no_one_win():
                                pygame.mixer.music.stop()
                                self.boo_sound.play()
                                self.state = config.GAME_STATES.NO_ONE_WIN
                            else: # It's the other player's turn if the current player didn't win
                                self.current_player = self.yellow_player if isinstance(self.current_player, objects.RedPlayer) else self.red_player

                            self.current_player_chip = None
                            self.current_player_chip_column = 0
                        else: # The column is full
                            self.column_full_sound.play()

            self.draw_title(self.current_player.name + ' player turn', self.current_player.color)
        elif self.state == config.GAME_STATES.WON:
            for event in pygame.event.get():
                utils.try_quit(event)

                if event.type == pygame.KEYDOWN:
                    self.init_new_game()

            self.draw_title(self.current_player.name + ' player win! Press any key to start a new game', config.COLORS.WHITE.value)
        elif self.state == config.GAME_STATES.NO_ONE_WIN:
            for event in pygame.event.get():
                utils.try_quit(event)

                if event.type == pygame.KEYDOWN:
                    self.init_new_game()

            self.draw_title('Shame, no one win. Press any key to start a new game', config.COLORS.WHITE.value)

        self.chips.draw(self.window)
        self.draw_board()

        pygame.display.update()

        self.clock.tick(config.FPS)
