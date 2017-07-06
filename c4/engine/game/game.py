#from screens import menu
import logging
import sys
from collections import deque

import pygame

import objects
import settings
import utils


class Game:
    def __init__(self, app):
        logging.info('Initializing game')

        self.app = app

        # the array of chips already placed on the game
        self.chips = pygame.sprite.Group()
        self.current_consecutive_chips = deque(maxlen=4)

        self.red_player = objects.RedPlayer()
        self.yellow_player = objects.YellowPlayer()

        logging.info('Loading images')

        self.board_cell_image = utils.load_image('board_cell.png')
        self.board_cell_highlighted_image = utils.load_image('board_cell_highlighted.png')

        logging.info('Loading sounds')

        self.sounds_volume = self.app.config.getfloat('connectfour', 'sounds_volume')
        self.musics_volume = self.app.config.getfloat('connectfour', 'music_volume')

        self.placed_sound = utils.load_sound('placed.wav', volume=self.sounds_volume)
        self.column_change_sound = utils.load_sound('column_change.wav', volume=self.sounds_volume)
        self.column_full_sound = utils.load_sound('column_full.wav', volume=self.sounds_volume)
        self.win_sound = utils.load_sound('win.wav', volume=self.sounds_volume)
        self.applause_sound = utils.load_sound('applause.wav', volume=self.sounds_volume)
        self.boo_sound = utils.load_sound('boo.wav', volume=self.sounds_volume)

        logging.info('Loading fonts')

        self.title_font = utils.load_font('Gidole-Regular.ttf', 22)
        self.normal_font = utils.load_font('Gidole-Regular.ttf', 16)

        self.init_new_game()

    def init_new_game(self):
        logging.info('Starting new game')

        self.program_state = settings.GAME_STATES.PLAYING

        self.chips.empty()
        self.current_consecutive_chips.clear()

        self.current_player = self.red_player # The starting player is always the red one
        self.current_player_chip = None
        self.current_player_chip_column = 0

        self.board = {}
        self.highlighted_chips = {}

        #self.game_problem = adversarial_search.ConnectFour()
        #self.game_state = self.game_problem.initial # the game state (used for reasoning).

        for x in range(0, settings.COLS):
            self.board[x] = {}
            self.highlighted_chips[x] = {}

            for y in range(0, settings.ROWS):
                self.board[x][y] = None
                self.highlighted_chips[x][y] = None

        logging.info('Loading random music')

        utils.load_random_music(['techno_dreaming.wav', 'techno_celebration.wav', 'electric_rain.wav', 'snake_trance.wav'], volume=self.musics_volume)

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
        elif cell != self.current_player.name:
            consecutive_chips = 0

        if consecutive_chips == 4:
            return consecutive_chips

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
                elif cell != self.current_player.name:
                    consecutive_chips = 0

                if consecutive_chips == 4:
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
                elif cell != self.current_player.name:
                    consecutive_chips = 0

                if consecutive_chips == 4:
                    return True

                previous_chip = cell

        self.current_consecutive_chips.clear()

        # Check each "/" diagonal starting at the top left corner
        x = 0

        for y in range(0, settings.ROWS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1))

            if consecutive_chips == 4:
                return True

        self.current_consecutive_chips.clear()

        # Check each "/" diagonal starting at the bottom left + 1 corner
        y = settings.ROWS - 1

        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1))

            if consecutive_chips == 4:
                return True

        self.current_consecutive_chips.clear()

        # Check each "\" diagonal starting at the bottom left corner
        x = 0

        for y in range(settings.ROWS, -1, -1):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1))

            if consecutive_chips == 4:
                return True

        self.current_consecutive_chips.clear()

        # Check each "\" diagonal starting at the top left + 1 corner
        y = 0

        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1))

            if consecutive_chips == 4:
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
        blue_rect_2 = pygame.Rect((0, settings.COLUMN_CHOOSING_MARGIN_TOP), (
        settings.WINDOW_SIZE[0], settings.IMAGES_SIDE_SIZE))

        self.app.window.fill(settings.COLORS.BLUE.value, blue_rect_1)
        self.app.window.fill(settings.COLORS.BLUE.value, blue_rect_2)

    def draw_header(self, status_text, status_color):
        # Status
        status = self.title_font.render(status_text, True, status_color)
        status_rect = status.get_rect()
        status_rect.x = 10
        status_rect.centery = 25

        self.app.window.blit(status, status_rect)

        # Game name
        game_name = self.normal_font.render('Connect Four v' + settings.VERSION, True, settings.COLORS.WHITE.value)
        game_name_rect = game_name.get_rect()
        game_name_rect.centery = 25
        game_name_rect.right = self.app.window.get_rect().width - 10

        self.app.window.blit(game_name, game_name_rect)

        # Scores
        pygame.draw.line(self.app.window, settings.COLORS.BLACK.value, (game_name_rect.left - 15, 0), (game_name_rect.left - 15, settings.COLUMN_CHOOSING_MARGIN_TOP - 1))

        scores_yellow = self.title_font.render(str(self.yellow_player.score), True, settings.COLORS.YELLOW.value)
        scores_yellow_rect = scores_yellow.get_rect()
        scores_yellow_rect.centery = 25
        scores_yellow_rect.right = game_name_rect.left - 25

        self.app.window.blit(scores_yellow, scores_yellow_rect)

        dash = self.title_font.render('-', True, settings.COLORS.WHITE.value)
        dash_rect = dash.get_rect()
        dash_rect.centery = 25
        dash_rect.right = scores_yellow_rect.left - 5

        self.app.window.blit(dash, dash_rect)

        scores_red = self.title_font.render(str(self.red_player.score), True, settings.COLORS.RED.value)
        scores_red_rect = scores_red.get_rect()
        scores_red_rect.centery = 25
        scores_red_rect.right = dash_rect.left - 5

        self.app.window.blit(scores_red, scores_red_rect)

        pygame.draw.line(self.app.window, settings.COLORS.BLACK.value, (scores_red_rect.left - 15, 0), (scores_red_rect.left - 15, settings.COLUMN_CHOOSING_MARGIN_TOP - 1))

    def print_board(self):
        """
        Print board to console
        :return:
        """
        board_mat = [['0' for x in range(7)] for y in range(6)]
        for row in self.board.keys():
            l_row = []
            for col,v in self.board[row].iteritems():
                if v is not None:
                    board_mat[col][row] = v[0]
        for row in range(len(board_mat)):
             logging.info(str(board_mat[row]))

    def convert_board_to_ai(self):
        """
        Converts the self.board into the desired format for the ai reasoning.
        :return: the board in the form of a dict of {(x, y): Player} entries,
        where Player is 'R' or 'Y', standing for 'Red' and 'Yellow' chips,
        respectively.
            The coordinates look as follows:
                0         x
                |------------->
                |
                |
                |
             y  v
        """
        converted_dict = {}
        for row in self.board.keys():
            for col, v in self.board[row].iteritems():
                if v is not None:
                    converted_dict[(row, col)] = v[0]
        return converted_dict

    def _move_chip_right(self):
        """Move chip to the right on the screen"""
        if self.program_state == settings.GAME_STATES.PLAYING and self.current_player_chip:
            self.column_change_sound.play()

            if self.current_player_chip.rect.right + settings.IMAGES_SIDE_SIZE <= settings.WINDOW_SIZE[
                0]:  # The chip will not go beyond the screen
                self.current_player_chip.rect.right += settings.IMAGES_SIDE_SIZE
                self.current_player_chip_column += 1
            else:  # The chip will go beyond the screen: put it in the far left
                self.current_player_chip.rect.left = 0
                self.current_player_chip_column = 0

    def _move_chip_left(self):
        """Move chip to the left on the screen"""
        if self.program_state == settings.GAME_STATES.PLAYING and self.current_player_chip:
            self.column_change_sound.play()

            if self.current_player_chip.rect.left - settings.IMAGES_SIDE_SIZE >= 0:  # The chip will not go beyond the screen
                self.current_player_chip.rect.left -= settings.IMAGES_SIDE_SIZE
                self.current_player_chip_column -= 1
            else:  # The chip will go beyond the screen: put it in the far right
                self.current_player_chip.rect.right = settings.WINDOW_SIZE[0]
                self.current_player_chip_column = settings.COLS - 1

    def _move_chip_down(self):
        """Move chip down on the screen (effectively perform player movement"""

        if self.program_state == settings.GAME_STATES.PLAYING and self.current_player_chip:
            # Check all rows in the currently selected column starting from the top
            chip_row_stop = self.get_free_row(self.current_player_chip_column)

            if chip_row_stop is not False:  # Actually move the chip in the current column and reset the current one (to create a new one later)
                self.placed_sound.play()
                self.board[self.current_player_chip_column][chip_row_stop] = self.current_player.name
                self.current_player_chip.rect.top += settings.IMAGES_SIDE_SIZE * (chip_row_stop + 1)

                if self.did_i_win():
                    self.set_highlighted_chips()
                    pygame.mixer.music.stop()
                    self.win_sound.play()
                    self.applause_sound.play()
                    self.program_state = settings.GAME_STATES.WON
                    pygame.time.set_timer(settings.EVENTS.WINNER_CHIPS_EVENT.value, 600)
                    logging.info(self.current_player.name + ' win')
                    self.current_player.score += 1
                elif self.did_no_one_win():
                    pygame.mixer.music.stop()
                    self.boo_sound.play()
                    self.program_state = settings.GAME_STATES.NO_ONE_WIN
                    logging.info('No one won')
                else:  # It's the other player's turn if the current player didn't win
                    self.current_player = self.yellow_player if isinstance(self.current_player,
                                                                           objects.RedPlayer) else self.red_player
                    logging.info(self.current_player.name + ' player turn')

                self.current_player_chip = None
                self.current_player_chip_column = 0
            else:  # The column is full
                self.column_full_sound.play()
                logging.info('{} column full'.format(self.current_player_chip_column))

    def update(self):
        self.draw_background()

        if self.program_state == settings.GAME_STATES.PLAYING:
            
            if not self.current_player_chip:
                self.current_player_chip = self.current_player.chip()

                self.chips.add(self.current_player_chip)
                self.current_player_chip.rect.left = 0
                self.current_player_chip.rect.top = settings.COLUMN_CHOOSING_MARGIN_TOP

            # If there is AI, call its get_move method.
            if self.current_player.id == 'AI':
                self.game_state, move = self.current_player.move(self.game_state, self.game_problem)
                for i in range(move[0]):
                    self._move_chip_right()
                self._move_chip_down()
                logging.info('AI Move: ' + str(move))
            else:

                # MOUSE INTERACTIVITY           
                if self.current_player_chip:
                    #self.column_change_sound.play()
                    mousex, mousey = pygame.mouse.get_pos()
                    col_clicked = (mousex / settings.IMAGES_SIDE_SIZE) \
                                  % settings.COLS
                    if (col_clicked >= 0) and (col_clicked < settings.COLS):
                        self.current_player_chip_column = col_clicked
                        self.current_player_chip.rect.right = settings.IMAGES_SIDE_SIZE * \
                                                              (self.current_player_chip_column+1) 
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE: # The user want to go back to the game menu
                            self.app.set_current_screen(menu.Menu, True)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # pygame.mouse.get_pressed() returns a tupple 
                        # (leftclick, middleclick, rightclick) Each one 
                        # is a boolean integer representing button up/down.
                        if pygame.mouse.get_pressed()[0]:
                            self._move_chip_down()
                            
            status_text = self.current_player.name + " PLAYER'S TURN!"
            status_color = self.current_player.color
        elif self.program_state == settings.GAME_STATES.WON:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # The user want to go back to the game menu
                        self.app.set_current_screen(menu.Menu, True)
                    elif event.key == pygame.K_RETURN: # Pressing the Return key will start a new game
                        self.init_new_game()
                elif event.type == settings.EVENTS.WINNER_CHIPS_EVENT.value:
                    for x in range(0, settings.COLS):
                        for y in range(0, settings.ROWS):
                            if isinstance(self.highlighted_chips[x][y], bool):
                                self.highlighted_chips[x][y] = not self.highlighted_chips[x][y]

                    pygame.time.set_timer(settings.EVENTS.WINNER_CHIPS_EVENT.value, 600)

            status_text = self.current_player.name + ' PLAYER WINS!'
            status_color = self.current_player.color
        elif self.program_state == settings.GAME_STATES.NO_ONE_WIN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # The user want to go back to the game menu
                        self.app.set_current_screen(menu.Menu, True)
                    elif event.key == pygame.K_RETURN: # Pressing the Return key will start a new game
                        self.init_new_game()

            status_text = 'TIE!'
            status_color = settings.COLORS.WHITE.value

        self.draw_header(status_text, status_color)
        self.chips.draw(self.app.window)
        self.draw_board()
