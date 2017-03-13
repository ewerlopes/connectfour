from configparser import ConfigParser
from screens.game import Game
from screens.menu import Menu
import masterserver
import pygame
import constants
import utils
import logging
import os
import sys


class App:
    def __init__(self):
        logging.info('Initializing app')

        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(constants.WINDOW_SIZE, pygame.DOUBLEBUF)

        pygame.display.set_caption('Connect Four ' + constants.VERSION)
        pygame.display.set_icon(utils.load_image('icon.png'))

        self.load_config()

        self.masterserver = masterserver.MasterServer(self.config.get('connectfour', 'master_server_endpoint'))

        self.load_screens()

    def try_to_quit(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    def load_config(self):
        logging.info('Loading configuration')

        self.config = ConfigParser(defaults=constants.DEFAULT_CONFIG)

        if os.path.isfile(constants.CONFIG_FILE):
            logging.info('Configuration file exist')

            self.config.read(constants.CONFIG_FILE)
        else:
            logging.info('Configuration file does not exist')

            with open(constants.CONFIG_FILE, 'w') as configfile:
                self.config.write(configfile)

    def load_screens(self):
        logging.info('Loading screens')

        self.menu_screen = Menu(self)
        self.game_screen = Game(self)

        self.current_screen = self.game_screen

    def update(self):
        self.current_screen.update()

        pygame.display.update()

        self.clock.tick(constants.FPS)
