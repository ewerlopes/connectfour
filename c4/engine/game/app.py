import logging
import os

import pygame
from configparser import ConfigParser

from c4.engine.game import view, utils, settings


class App:
    def __init__(self, dev_mode=False, no_sounds=False):
        logging.info('Initializing app')

        self.dev_mode = dev_mode
        self.no_sounds = no_sounds

        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(settings.WINDOW_SIZE, pygame.DOUBLEBUF)

        pygame.display.set_caption('Connect Four ' + settings.VERSION)
        pygame.display.set_icon(utils.load_image('icon.png'))

        self.load_config()
        self.set_current_screen(view.View)

    def load_config(self):
        logging.info('Loading configuration')

        self.config = ConfigParser(defaults=settings.DEFAULT_CONFIG, interpolation=None)

        if os.path.isfile(settings.CONFIG_FILE):
            logging.info('Configuration file exist')

            self.config.read(settings.CONFIG_FILE)
        else:
            logging.info('Configuration file does not exist')

            self.config.add_section('connectfour')

            with open(settings.CONFIG_FILE, 'w') as configfile:
                self.config.write(configfile)

    def set_current_screen(self, Screen, *args):
        logging.info('Setting current screen to {}'.format(Screen))
        if hasattr(self, 'current_screen') and self.current_screen:
            del self.current_screen
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        self.current_screen = Screen(self, *args)

    def update(self):
        self.current_screen.update()

        pygame.display.update()

        self.clock.tick(settings.FPS)
