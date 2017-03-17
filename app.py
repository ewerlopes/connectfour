from configparser import ConfigParser
from screens import menu
from networking import cfms
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

        self.master_server_client = cfms.Client(self.config.get('connectfour', 'master_server_endpoint'))

        self.set_current_screen(menu.Menu)

    def load_config(self):
        logging.info('Loading configuration')

        self.config = ConfigParser(defaults=constants.DEFAULT_CONFIG)

        if os.path.isfile(constants.CONFIG_FILE):
            logging.info('Configuration file exist')

            self.config.read(constants.CONFIG_FILE)
        else:
            logging.info('Configuration file does not exist')

            self.config.add_section('connectfour')

            with open(constants.CONFIG_FILE, 'w') as configfile:
                self.config.write(configfile)

    def set_current_screen(self, Screen, *args):
        logging.info('Setting current screen to {}'.format(Screen))

        if hasattr(self, 'current_screen') and self.current_screen:
            del self.current_screen

        self.current_screen = Screen(self, *args)

    def update(self):
        self.current_screen.update()

        pygame.display.update()

        self.clock.tick(constants.FPS)
