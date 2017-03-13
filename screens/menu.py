import pygame
import logging
import constants
import gui
import utils
import sys


class Menu:
    def __init__(self, app):
        logging.info('Initializing menu')

        self.app = app
        self.gui = pygame.sprite.Group()

        logging.info('Loading fonts')

        self.title_font = utils.load_font('monofur.ttf', 62)
        self.normal_font = utils.load_font('monofur.ttf', 16)

        logging.info('Loading GUI')

        btn_local_game_rect = pygame.Rect(0, 200, 200, 40)
        btn_local_game_rect.centerx = self.app.window.get_rect().centerx

        btn_local_game = gui.Button(
            rect=btn_local_game_rect,
            font=self.normal_font,
            text='Local game',
            text_color=constants.COLORS.WHITE.value,
            background_color=constants.COLORS.BLUE.value,
            border_color=constants.COLORS.RED.value
        )

        self.gui.add(btn_local_game)

        btn_host_game_rect = pygame.Rect(0, 300, 200, 40)
        btn_host_game_rect.centerx = self.app.window.get_rect().centerx

        btn_host_game = gui.Button(
            rect=btn_host_game_rect,
            font=self.normal_font,
            text='Host a game',
            text_color=constants.COLORS.WHITE.value,
            background_color=constants.COLORS.BLUE.value,
            border_color=constants.COLORS.RED.value
        )

        self.gui.add(btn_host_game)

        btn_join_game_rect = pygame.Rect(0, 400, 200, 40)
        btn_join_game_rect.centerx = self.app.window.get_rect().centerx

        btn_join_game = gui.Button(
            rect=btn_join_game_rect,
            font=self.normal_font,
            text='Join a game',
            text_color=constants.COLORS.WHITE.value,
            background_color=constants.COLORS.BLUE.value,
            border_color=constants.COLORS.RED.value
        )

        self.gui.add(btn_join_game)

    def draw_title(self):
        title = self.title_font.render('Connect Four ', True, constants.COLORS.WHITE.value)
        title_rect = title.get_rect()
        title_rect.centerx = self.app.window.get_rect().centerx
        title_rect.top = 25

        self.app.window.blit(title, title_rect)

        version = self.normal_font.render('v' + constants.VERSION, True, constants.COLORS.WHITE.value)
        version_rect = version.get_rect()
        version_rect.topright = title_rect.bottomright

        self.app.window.blit(version, version_rect)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        self.app.window.fill(constants.COLORS.BLACK.value)

        self.draw_title()

        self.gui.draw(self.app.window)
