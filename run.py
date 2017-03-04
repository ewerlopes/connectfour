import pygame
import config
import game
import utils
import logging
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    stream=sys.stdout
)

logging.getLogger().setLevel(logging.INFO)

logging.info('Initializing PyGame/{} (with SDL/{})'.format(
    pygame.version.ver,
    '.'.join(str(v) for v in pygame.get_sdl_version())
))

pygame.init()

logging.info('Initializing main window')

pygame.display.set_caption('Connect Four')

clock = pygame.time.Clock()
window = pygame.display.set_mode(config.WINDOW_SIZE, pygame.DOUBLEBUF)

pygame.display.set_icon(utils.load_image('icon.png'))

game = game.Game(window, clock)

logging.info('Running game')

while True:
    game.play()
