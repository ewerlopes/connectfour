from screens import menu
from collections import deque
import objects
import pygame
import settings
import utils
import logging
import sys


class Game:
    def __init__(self, app):
        logging.info('Initializing game')

        self.app = app

        self.chips = pygame.sprite.Group()
        self.current_consecutive_chips = deque(maxlen=4)
        self.red_player = objects.RedPlayer()
        self.yellow_player = objects.YellowPlayer()

        logging.info('Loading images')

        self.board_cell_image = utils.load_image('board_cell.png')
        self.board_cell_highlighted_image = utils.load_image('board_cell_highlighted.png')

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

        self.state = settings.GAME_STATES.PLAYING

        self.chips.empty()
        self.current_consecutive_chips.clear()

        self.current_player = self.red_player # The starting player is always the red one
        self.current_player_chip = None
        self.current_player_chip_column = 0

        self.board = {}
        self.highlighted_chips = {}

        for x in range(0, settings.COLS):
            self.board[x] = {}
            self.highlighted_chips[x] = {}

            for y in range(0, settings.ROWS):
                self.board[x][y] = None
                self.highlighted_chips[x][y] = None

        logging.info('Loading random music')

        utils.load_random_music(['techno_dreaming.wav', 'techno_celebration.wav', 'electric_rain.wav', 'snake_trance.wav'])

    def draw_game_name(self):
        text = self.normal_font.render('Connect Four v' + settings.VERSION, True, settings.COLORS.WHITE.value)
        text_rect = text.get_rect()
        text_rect.centery = 25
        text_rect.right = self.app.window.get_rect().width - 10

        self.app.window.blit(text, text_rect)

    def draw_status(self, text, color):
        text = self.title_font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.centery = 25

        self.app.window.blit(text, text_rect)

    def is_valid_position(self, x, y):
        if x < 0 or x > settings.COLS - 1 or y < 0 or y > settings.ROWS - 1:
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
            self.current_consecutive_chips.append((x, y))
            consecutive_chips = 1
        elif cell == self.current_player.name and cell == previous_chip:
            self.current_consecutive_chips.append((x, y))
            consecutive_chips += 1

        x, y = self.compute_direction_pos(x, y, direction)

        previous_chip = cell

        return self.count_consecutive_diagonal_chips(consecutive_chips, previous_chip, x, y, direction)

    def set_highlighted_chips(self):
        for chips_position in list(self.current_consecutive_chips):
            self.highlighted_chips[chips_position[0]][chips_position[1]] = True

    def did_i_win(self):
        """Check if the current player win the game.

        This method performs the checks on the whole board in all possible direction until 4 consecutive chips are found
        for the current player.
        """

        # Check each columns from left to right
        for x in range(0, settings.COLS):
            consecutive_chips = 0
            previous_chip = None

            for y in range(0, settings.ROWS):
                cell = self.board[x][y]

                if cell == self.current_player.name and consecutive_chips == 0:
                    self.current_consecutive_chips.append((x, y))
                    consecutive_chips = 1
                elif cell == self.current_player.name and cell == previous_chip:
                    self.current_consecutive_chips.append((x, y))
                    consecutive_chips += 1

                if consecutive_chips == 4:
                    self.set_highlighted_chips()
                    return True

                previous_chip = cell

        self.current_consecutive_chips.clear()

        # Check each rows from top to bottom
        for y in range(0, settings.ROWS):
            consecutive_chips = 0
            previous_chip = None

            for x in range(0, settings.COLS):
                cell = self.board[x][y]

                if cell == self.current_player.name and consecutive_chips == 0:
                    self.current_consecutive_chips.append((x, y))
                    consecutive_chips = 1
                elif cell == self.current_player.name and cell == previous_chip:
                    self.current_consecutive_chips.append((x, y))
                    consecutive_chips += 1

                if consecutive_chips == 4:
                    self.set_highlighted_chips()
                    return True

                previous_chip = cell

        self.current_consecutive_chips.clear()

        # Check each "/" diagonal starting at the top left corner
        x = 0

        for y in range(0, settings.ROWS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1))

            if consecutive_chips == 4:
                self.set_highlighted_chips()
                return True

        self.current_consecutive_chips.clear()

        # Check each "/" diagonal starting at the bottom left + 1 corner
        y = settings.ROWS - 1

        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1))

            if consecutive_chips == 4:
                self.set_highlighted_chips()
                return True

        self.current_consecutive_chips.clear()

        # Check each "\" diagonal starting at the bottom left corner
        x = 0

        for y in range(settings.ROWS, -1, -1):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1))

            if consecutive_chips == 4:
                self.set_highlighted_chips()
                return True

        self.current_consecutive_chips.clear()

        # Check each "\" diagonal starting at the top left + 1 corner
        y = 0

        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1))

            if consecutive_chips == 4:
                self.set_highlighted_chips()
                return True

        self.current_consecutive_chips.clear()

        return False

    def did_no_one_win(self):
        """Check if no one win the game.

        This method checks every single cell. If all are filled, no one win."""
        for x in range(0, settings.COLS):
            for y in range(0, settings.ROWS):
                if not self.board[x][y]: # The cell is empty: players still can play
                    return False

        return True

    def draw_board(self):
        """Draw the board itself (the game support)."""
        for x in range(0, settings.COLS):
            for y in range(0, settings.ROWS):
                if self.highlighted_chips[x][y] is True:
                    image = self.board_cell_highlighted_image
                else:
                    image = self.board_cell_image

                self.app.window.blit(image, (x * settings.IMAGES_SIDE_SIZE, y * settings.IMAGES_SIDE_SIZE + settings.BOARD_MARGIN_TOP))

    def get_free_row(self, column):
        """Given a column, get the latest row number which is free."""
        for y, cell in self.board[column].items():
            # If there's nothing in the current cell
            if not cell:
                # If we're in the latest cell or if the next cell isn't empty
                if (y == settings.ROWS - 1) or (not y + 1 > settings.ROWS - 1 and self.board[column][y + 1]):
                    return y

        return False

    def draw_background(self):
        self.app.window.fill(settings.COLORS.BLACK.value)

        blue_rect_1 = pygame.Rect((0, 0), (settings.WINDOW_SIZE[0], settings.COLUMN_CHOOSING_MARGIN_TOP - 1))
        blue_rect_2 = pygame.Rect((0, settings.COLUMN_CHOOSING_MARGIN_TOP), (settings.WINDOW_SIZE[0], settings.IMAGES_SIDE_SIZE))

        self.app.window.fill(settings.COLORS.BLUE.value, blue_rect_1)
        self.app.window.fill(settings.COLORS.BLUE.value, blue_rect_2)

    def update(self):
        self.draw_background()
        self.draw_game_name()

        if self.state == settings.GAME_STATES.PLAYING:
            if not self.current_player_chip:
                self.current_player_chip = self.current_player.chip()

                self.chips.add(self.current_player_chip)
                self.current_player_chip.rect.left = 0
                self.current_player_chip.rect.top = settings.COLUMN_CHOOSING_MARGIN_TOP

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # The user want to go back to the game menu
                        self.app.set_current_screen(menu.Menu)
                    elif event.key == pygame.K_LEFT: # Move chip to the left
                        self.column_change_sound.play()

                        if self.current_player_chip.rect.left - settings.IMAGES_SIDE_SIZE >= 0: # The chip will not go beyond the screen
                            self.current_player_chip.rect.left -= settings.IMAGES_SIDE_SIZE
                            self.current_player_chip_column -= 1
                        else: # The chip will go beyond the screen: put it in the far right
                            self.current_player_chip.rect.right = settings.WINDOW_SIZE[0]
                            self.current_player_chip_column = settings.COLS - 1
                    elif event.key == pygame.K_RIGHT: # Move chip to the right
                        self.column_change_sound.play()

                        if self.current_player_chip.rect.right + settings.IMAGES_SIDE_SIZE <= settings.WINDOW_SIZE[0]: # The chip will not go beyond the screen
                            self.current_player_chip.rect.right += settings.IMAGES_SIDE_SIZE
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
                            self.current_player_chip.rect.top += settings.IMAGES_SIDE_SIZE * (chip_row_stop + 1)

                            if self.did_i_win():
                                pygame.mixer.music.stop()
                                self.win_sound.play()
                                self.applause_sound.play()
                                self.state = settings.GAME_STATES.WON
                                pygame.time.set_timer(settings.EVENTS.WINNER_CHIPS_EVENT.value, 600)
                                logging.info(self.current_player.name + ' win')
                            elif self.did_no_one_win():
                                pygame.mixer.music.stop()
                                self.boo_sound.play()
                                self.state = settings.GAME_STATES.NO_ONE_WIN
                                logging.info('No one won')
                            else: # It's the other player's turn if the current player didn't win
                                self.current_player = self.yellow_player if isinstance(self.current_player, objects.RedPlayer) else self.red_player
                                logging.info(self.current_player.name + ' player turn')

                            self.current_player_chip = None
                            self.current_player_chip_column = 0
                        else: # The column is full
                            self.column_full_sound.play()
                            logging.info('{} column full'.format(self.current_player_chip_column))

            self.draw_status(self.current_player.name + ' player turn', self.current_player.color)
        elif self.state == settings.GAME_STATES.WON:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # The user want to go back to the game menu
                        self.app.set_current_screen(menu.Menu)
                    else:
                        self.init_new_game()
                elif event.type == settings.EVENTS.WINNER_CHIPS_EVENT.value:
                    for x in range(0, settings.COLS):
                        for y in range(0, settings.ROWS):
                            if isinstance(self.highlighted_chips[x][y], bool):
                                self.highlighted_chips[x][y] = not self.highlighted_chips[x][y]

                    pygame.time.set_timer(settings.EVENTS.WINNER_CHIPS_EVENT.value, 600)

            self.draw_status(self.current_player.name + ' player win!', settings.COLORS.WHITE.value)
        elif self.state == settings.GAME_STATES.NO_ONE_WIN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # The user want to go back to the game menu
                        self.app.set_current_screen(menu.Menu)
                    else:
                        self.init_new_game()

            self.draw_status('Shame, no one win.', settings.COLORS.WHITE.value)

        self.chips.draw(self.app.window)
        self.draw_board()
