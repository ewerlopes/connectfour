from screens import menu
import pygame
import logging
import constants
import utils
import sys
import platform


class Lobby:
    def __init__(self, app, lobby_type):
        logging.info('Initializing lobby')

        self.app = app
        self.lobby_type = lobby_type

        logging.info('Type: {}'.format(self.lobby_type))

        logging.info('Loading fonts')

        self.title_font = utils.load_font('monofur.ttf', 24)
        self.normal_font = utils.load_font('monofur.ttf', 18)

        if self.lobby_type == constants.LOBBY_STATES.HOST_ONLINE_GAME:
            self.create_game()
        elif self.lobby_type == constants.LOBBY_STATES.JOIN_ONLINE_GAME:
            self.games = []
            self.get_games()

    def get_games(self):
        logging.info('Getting games list')

        try:
            self.games = self.app.master_server_client.get_games(constants.VERSION)
        except Exception as e:
            logging.error(e)

    def create_game(self):
        if not hasattr(self.app, 'current_online_game'):
            logging.info('Creating a new online game')

            try:
                self.app.current_online_game = self.app.master_server_client.create_game(platform.node(), constants.VERSION)

                # TODO Start a looping thread that POST to /games/{id} every 3 minutes without any parameter (to update the last_ping_at attribute)
            except Exception as e:
                logging.error(e)

    def delete_game(self):
        if hasattr(self.app, 'current_online_game') and self.app.current_online_game:
            logging.info('Deleting the current game #{}'.format(self.app.current_online_game['id']))

            try:
                self.app.master_server_client.delete_game(self.app.current_online_game['id'], self.app.current_online_game['token'])

                del self.app.current_online_game

                # TODO Kill the looping thread that POST to /games/{id} every 3 minutes
            except Exception as e:
                logging.error(e)
        else:
            logging.info('No current game to delete')

    def update(self):
        for event in pygame.event.get():
            if self.lobby_type == constants.LOBBY_STATES.HOST_ONLINE_GAME:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.delete_game()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # The user want to go back to the game menu
                    self.app.set_current_screen(menu.Menu)

        self.app.window.fill(constants.COLORS.BLACK.value)

        if self.lobby_type == constants.LOBBY_STATES.HOST_ONLINE_GAME:
            self.draw_title('Host an online game')
        elif self.lobby_type == constants.LOBBY_STATES.JOIN_ONLINE_GAME:
            self.draw_title('Join an online game')

            y = 50

            for game in self.games:
                game_name = self.normal_font.render(game['name'], True, constants.COLORS.WHITE.value)
                game_name_rect = game_name.get_rect()
                game_name_rect.left = 10
                game_name_rect.top = y

                self.app.window.blit(game_name, game_name_rect)

                game_ip = self.normal_font.render(game['ip'] + ' (' + game['country'] + ')', True, constants.COLORS.WHITE.value)
                game_ip_rect = game_ip.get_rect()
                game_ip_rect.right = constants.WINDOW_SIZE[0] - 10
                game_ip_rect.top = y

                self.app.window.blit(game_ip, game_ip_rect)

                y += 50

    def draw_title(self, text):
        title = self.title_font.render(text, True, constants.COLORS.WHITE.value)
        title_rect = title.get_rect()
        title_rect.left = 10
        title_rect.top = 10

        self.app.window.blit(title, title_rect)
