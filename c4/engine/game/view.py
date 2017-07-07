from collections import deque

from c4.engine.search.searchProblem import Connect4
from c4.engine.ai import (
    GreedyEngine, WeightedGreedyEngine, RandomEngine,
    MonteCarloTreeSearch,
    NegamaxEngine, AlphaBetaEngine, ABCachedEngine, ABDeepEngine,
    PVSEngine, PVSCachedEngine, PVSDeepEngine, HumanEngine
)

import logging
import sys
import pygame
import objects
import settings
import utils

engine_map = {
    'greedy': GreedyEngine,
    'weighted': WeightedGreedyEngine,
    'mcts': MonteCarloTreeSearch,
    'random': RandomEngine,
    'negamax': NegamaxEngine,
    'alphabeta': AlphaBetaEngine,
    'abcached': ABCachedEngine,
    'abdeep': ABDeepEngine,
    'pvs': PVSEngine,
    'pvscached': PVSCachedEngine,
    'pvsdeep': PVSDeepEngine,
    'human'  : HumanEngine
    }


class View:
    def __init__(self, app):
        logging.info('Initializing game')

        self.app = app

        # the array of chips already placed on the game
        self.chips = pygame.sprite.Group()
        self.current_consecutive_chips = deque(maxlen=4)

        self.game_problem = Connect4()
        
        self.engine1 = engine_map['alphabeta']()
        self.engine2 = engine_map['abdeep']()
        
        self.players = {
            Connect4.PLAYER1_ID: objects.RedPlayer(self.engine1),
            Connect4.PLAYER2_ID: objects.YellowPlayer(self.engine2)
        }
        
        self.previous_move_failed = False
        
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

        self.new_game()

    def new_game(self):
        logging.info('Starting new game')
        self.program_state = settings.GAME_STATES.PLAYING

        self.game_problem = Connect4()
        self.chips.empty()
        self.current_consecutive_chips.clear()

        self.current_player = self.players[Connect4.PLAYER1_ID]  # The starting player (always RED).
        self.current_player_chip = None
        self.current_player_chip_column = 0

        self.previous_move_failed = False
        
        self.highlighted_chips = {}

        logging.info('Loading random music')
        utils.load_random_music(['techno_dreaming.wav', 'techno_celebration.wav', 'electric_rain.wav', 'snake_trance.wav'], volume=self.musics_volume)
        

    def set_highlighted_chips(self):
        for chips_position in list(self.current_consecutive_chips):
            self.highlighted_chips[chips_position[0]][chips_position[1]] = True

    def draw_board(self):
        """Draw the board itself (the game support)."""
        board = self.game_problem.get_board()
        for x in range(0, settings.COLS):
            for y in range(0, settings.ROWS):
                if (y,x) in self.highlighted_chips.keys() and self.highlighted_chips[(y,x)]:
                    image = self.board_cell_highlighted_image
                else:
                    image = self.board_cell_image

                self.app.window.blit(image, (x * settings.IMAGES_SIDE_SIZE, y * settings.IMAGES_SIDE_SIZE + settings.BOARD_MARGIN_TOP))

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

        scores_yellow = self.title_font.render(str(self.players[Connect4.PLAYER2_ID].score), True, settings.COLORS.YELLOW.value)
        scores_yellow_rect = scores_yellow.get_rect()
        scores_yellow_rect.centery = 25
        scores_yellow_rect.right = game_name_rect.left - 25

        self.app.window.blit(scores_yellow, scores_yellow_rect)

        dash = self.title_font.render('-', True, settings.COLORS.WHITE.value)
        dash_rect = dash.get_rect()
        dash_rect.centery = 25
        dash_rect.right = scores_yellow_rect.left - 5

        self.app.window.blit(dash, dash_rect)

        scores_red = self.title_font.render(str(self.players[Connect4.PLAYER1_ID].score), True, settings.COLORS.RED.value)
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

    def get_row(self, column):
        """Given a column, get the latest row number which is free."""
        for y in range(0, settings.ROWS):
            # If there's nothing in the current cell
            cell = self.game_problem.get_board()[y][column]
            if cell:
                return y
        return False

    def _place_chip(self, col):
        """Move chip down on the screen (effectively perform player movement"""

        if self.program_state == settings.GAME_STATES.PLAYING and self.current_player_chip:
            # Check all rows in the currently selected column starting from the top
            chip_row_stop = self.get_row(col)

            if chip_row_stop is not False:  # Actually move the chip in the current column and reset the current one (to create a new one later)
                self.placed_sound.play()
                self.current_player_chip_column = col
                self.current_player_chip.rect.right = settings.IMAGES_SIDE_SIZE * \
                                                      (self.current_player_chip_column + 1)
                self.current_player_chip.rect.top += settings.IMAGES_SIDE_SIZE * (chip_row_stop + 1)
                self.current_player_chip = None
                self.current_player_chip_column = 0
                self.previous_move_failed = False
                logging.info('Movement SUCCEEDED!')
                logging.info("-- BOARD: ")
                board = self.game_problem.get_board()
                for i in range(len(board)):
                    logging.info(board[i])
            else:  # The column is full
                self.column_full_sound.play()
                self.previous_move_failed = True
                logging.info('Movement FAILED {} column full.'.format(col))

    def update(self):
        self.draw_background()

        if self.program_state == settings.GAME_STATES.PLAYING:
            
            if not self.current_player_chip:
                logging.info(self.current_player.name + ' player turn')
                self.current_player_chip = self.current_player.chip()

                self.chips.add(self.current_player_chip)
                self.current_player_chip.rect.left = 0
                self.current_player_chip.rect.top = settings.COLUMN_CHOOSING_MARGIN_TOP

            status_text = self.current_player.name + " PLAYER'S TURN!"
            status_color = self.current_player.color
            
            move = self.current_player.engine.choose(self.game_problem)
            self.game_problem = self.game_problem.move(move)
            self._place_chip(move)

            if self.game_problem.end == Connect4.DRAW_ID:
                pygame.mixer.music.stop()
                self.boo_sound.play()
                self.program_state = settings.GAME_STATES.NO_ONE_WIN
                logging.info('No one won')
            elif self.game_problem.end is None and not self.previous_move_failed: # It's the other player's turn if the current player didn't win
                self.current_player = self.players[self.game_problem.whose_turn_is_it]
                logging.info('Starting new player turn')
            elif self.game_problem.end == Connect4.PLAYER1_ID or self.game_problem.end == Connect4.PLAYER2_ID:
                pygame.mixer.music.stop()
                self.win_sound.play()
                self.program_state = settings.GAME_STATES.WON
                pygame.time.set_timer(settings.EVENTS.WINNER_CHIPS_EVENT.value, 600)
                logging.info(self.current_player.name + ' WINS!')
                self.current_player.score += 1
                self.highlighted_chips = Connect4.get_win_segment(self.game_problem._board)

            
        elif self.program_state == settings.GAME_STATES.WON:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # The user want to go back to the game menu
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN: # Pressing the Return key will start a new game
                        self.new_game()
                elif event.type == settings.EVENTS.WINNER_CHIPS_EVENT.value:
                    for k in self.highlighted_chips.keys():
                        self.highlighted_chips[k] = not self.highlighted_chips[k]

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
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN: # Pressing the Return key will start a new game
                        self.new_game()

            status_text = 'TIE!'
            status_color = settings.COLORS.WHITE.value

        self.draw_header(status_text, status_color)
        self.chips.draw(self.app.window)
        self.draw_board()
