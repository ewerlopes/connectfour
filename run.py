import logging
import os
import sys

import click
import pygame

from c4.engine.game.app import App


@click.command()
@click.option('--muted', is_flag=True, default=False, help='No sounds')
@click.option('--dev', is_flag=True, default=False, help='Dev mode')
def run(muted, dev):
    os.environ['SDL_VIDEO_CENTERED'] = '1' # This makes the window centered on the screen

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        stream=sys.stdout
    )

    logging.getLogger().setLevel(logging.DEBUG if dev else logging.WARNING)

    logging.info('Initializing PyGame/{} (with SDL/{})'.format(
        pygame.version.ver,
        '.'.join(str(v) for v in pygame.get_sdl_version())
    ))

    pygame.init()

    if dev:
        logging.info('Dev mode enabled')

    if muted:
        logging.info('Running with no sounds')

    app = App(dev_mode=dev, no_sounds=muted)

    logging.info('Running game')

    while True:
        app.update()

if __name__ == '__main__':
    run()
