from configparser import ConfigParser
from screens.game import Game
from screens.menu import Menu
import masterserver
import pygame
import constants
import utils
import logging
import os


class App:
    def __init__(self):
        logging.info('Initializing app')

        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(constants.WINDOW_SIZE, pygame.DOUBLEBUF)

        pygame.display.set_caption('Connect Four ' + constants.VERSION)
        pygame.display.set_icon(utils.load_image('icon.png'))

        self.load_config()

        self.masterserver = masterserver.MasterServer(self.get_config('master_server_endpoint'))

        self.set_current_screen(Game)
        # self.set_current_screen(Menu)

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

    def get_config(self, key):
        return self.config.get('connectfour', key)

    def set_current_screen(self, Screen):
        logging.info('Setting current screen to {}'.format(Screen))

        if hasattr(self, 'current_screen') and self.current_screen:
            del self.current_screen

        self.current_screen = Screen(self)

    def update(self):
        self.current_screen.update()

        pygame.display.update()

        self.clock.tick(constants.FPS)
