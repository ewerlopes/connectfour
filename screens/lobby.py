from screens import menu
from networking import lan
import pygame
import logging
import settings
import utils
import sys
import platform
import gui


class Lobby:
    def __init__(self, app, lobby_type):
        logging.info('Initializing lobby')

        self.app = app
        self.lobby_type = lobby_type

        logging.info('Type: {}'.format(self.lobby_type))

        logging.info('Loading fonts')

        self.title_font = utils.load_font('monofur.ttf', 24)
        self.normal_font = utils.load_font('monofur.ttf', 18)

        gui.init()

        self.gui_container = pygame.sprite.Group()

        if self.lobby_type == settings.LOBBY_STATES.HOST_ONLINE_GAME:
            self.create_online_game()
        elif self.lobby_type == settings.LOBBY_STATES.JOIN_ONLINE_GAME:
            self.games = []
            self.get_online_games()
        elif self.lobby_type == settings.LOBBY_STATES.HOST_LAN_GAME:
            self.lan_announcer = lan.Announcer()
        elif self.lobby_type == settings.LOBBY_STATES.JOIN_LAN_GAME:
            self.lan_discoverer = lan.Discoverer()

    def get_online_games(self):
        logging.info('Getting online games list')

        try:
            self.games = self.app.master_server_client.get_games(settings.VERSION)
        except Exception as e:
            logging.error(e)

    def create_online_game(self):
        if not hasattr(self.app, 'current_online_game'):
            logging.info('Creating a new online game')

            try:
                self.app.current_online_game = self.app.master_server_client.create_game(platform.node(), settings.VERSION)

                # TODO Start a looping thread that POST to /games/{id} every 3 minutes without any parameter (to update the last_ping_at attribute)
            except Exception as e:
                logging.error(e)

    def delete_online_game(self):
        if hasattr(self.app, 'current_online_game') and self.app.current_online_game:
            logging.info('Deleting the current online game #{}'.format(self.app.current_online_game['id']))

            try:
                self.app.master_server_client.delete_game(self.app.current_online_game['id'], self.app.current_online_game['token'])

                del self.app.current_online_game

                # TODO Kill the looping thread that POST to /games/{id} every 3 minutes
            except Exception as e:
                logging.error(e)
        else:
            logging.info('No current online game to delete')

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                if self.lobby_type == settings.LOBBY_STATES.HOST_ONLINE_GAME:
                    self.delete_online_game()
                elif self.lobby_type == settings.LOBBY_STATES.HOST_LAN_GAME:
                    self.lan_announcer.stop()
                    del self.lan_announcer
                elif self.lobby_type == settings.LOBBY_STATES.JOIN_LAN_GAME:
                    self.lan_discoverer.stop()
                    del self.lan_discoverer

            gui.event_handler(self.gui_container, event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # The user want to go back to the game menu
                    self.app.set_current_screen(menu.Menu)

        self.app.window.fill(settings.COLORS.BLACK.value)

        if self.lobby_type == settings.LOBBY_STATES.HOST_ONLINE_GAME:
            self.draw_title('Host an online game')
        elif self.lobby_type == settings.LOBBY_STATES.JOIN_ONLINE_GAME:
            self.draw_title('Join an online game')

            y = 50

            for game in self.games:
                game_name = self.normal_font.render(game['name'], True, settings.COLORS.WHITE.value)
                game_name_rect = game_name.get_rect()
                game_name_rect.left = 10
                game_name_rect.top = y

                self.app.window.blit(game_name, game_name_rect)

                game_ip = self.normal_font.render(game['ip'] + ' (' + game['country'] + ')', True, settings.COLORS.WHITE.value)
                game_ip_rect = game_ip.get_rect()
                game_ip_rect.right = settings.WINDOW_SIZE[0] - 10
                game_ip_rect.top = y

                self.app.window.blit(game_ip, game_ip_rect)

                y += 50

        self.gui_container.update()
        self.gui_container.draw(self.app.window)

    def draw_title(self, text):
        title = self.title_font.render(text, True, settings.COLORS.WHITE.value)
        title_rect = title.get_rect()
        title_rect.left = 10
        title_rect.top = 10

        self.app.window.blit(title, title_rect)
