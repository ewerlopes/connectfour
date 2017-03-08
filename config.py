from enum import Enum
import pygame
import sys
import os

VERSION = '1.0'
FPS = 60
IMAGES_SIDE_SIZE = 112
COLS = 7
ROWS = 6
COLUMN_CHOOSING_MARGIN_TOP = 50
BOARD_MARGIN_TOP = IMAGES_SIDE_SIZE + COLUMN_CHOOSING_MARGIN_TOP
WINDOW_SIZE = (IMAGES_SIDE_SIZE * COLS, (IMAGES_SIDE_SIZE * ROWS) + BOARD_MARGIN_TOP)
SOUNDS_VOLUME = 0.1
MUSIC_VOLUME = 0.2

# When frozen by PyInstaller, the path to the resources is different
RESOURCES_ROOT = os.path.join(sys._MEIPASS, 'resources') if getattr(sys, 'frozen', False) else 'resources'


class COLORS(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 174, 0),
    BLUE = (0, 42, 224)


class GAME_STATES(Enum):
    PLAYING = 2
    WON = 4
    NO_ONE_WIN = 5


class EVENTS(Enum):
    WINNER_CHIPS_EVEN = pygame.USEREVENT + 2
