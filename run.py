from app import App
import pygame
import logging
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1' # This makes the window centered on the screen

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

app = App()

logging.info('Running game')

while True:
    app.update()
