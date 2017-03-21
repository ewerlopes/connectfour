from screens import game
from screens import lobby
import pygame
import logging
import settings
import gui
import utils
import sys


class Menu:
    def __init__(self, app, force_music=False):
        logging.info('Initializing menu')

        self.app = app

        logging.info('Loading fonts')

        self.title_font = utils.load_font('monofur.ttf', 62)
        self.normal_font = utils.load_font('monofur.ttf', 18)

        self.musics_volume = self.app.config.getfloat('connectfour', 'music_volume')

        if not pygame.mixer.music.get_busy() or force_music:
            utils.load_music('menu.wav', volume=self.musics_volume)

        self.load_gui()

    def create_menu_button(self, y, text, on_click, disabled=False):
        btn_rect = pygame.Rect(0, y, 200, 40)
        btn_rect.centerx = self.app.window.get_rect().centerx

        return gui.Button(
            rect=btn_rect,
            font=self.normal_font,
            text=text,
            on_click=on_click,
            disabled=disabled
        )

    def btn_offline_game_click(self):
        logging.info('Offline game button clicked')

        self.app.set_current_screen(game.Game)

    def btn_host_online_game_click(self):
        logging.info('Host an online game button clicked')

        self.app.set_current_screen(lobby.Lobby, settings.LOBBY_STATES.HOST_ONLINE_GAME)

    def btn_join_online_game_click(self):
        logging.info('Join an online game button clicked')

        self.app.set_current_screen(lobby.Lobby, settings.LOBBY_STATES.JOIN_ONLINE_GAME)

    def btn_host_lan_game_click(self):
        logging.info('Host a LAN game button clicked')

        self.app.set_current_screen(lobby.Lobby, settings.LOBBY_STATES.HOST_LAN_GAME)

    def btn_join_lan_game_click(self):
        logging.info('Join a LAN game button clicked')

        self.app.set_current_screen(lobby.Lobby, settings.LOBBY_STATES.JOIN_LAN_GAME)

    def btn_quit_click(self):
        pygame.quit()
        sys.exit()

    def load_gui(self):
        gui.init(theme=settings.GuiTheme(sounds_volume=self.app.config.getfloat('connectfour', 'sounds_volume')))

        self.gui_container = pygame.sprite.Group()

        # Offline game button
        self.gui_container.add(self.create_menu_button(
            y=120,
            text='Offline game',
            on_click=self.btn_offline_game_click
        ))

        # Host an online game button
        self.gui_container.add(self.create_menu_button(
            y=180,
            text='Host an online game',
            on_click=self.btn_host_online_game_click,
            disabled=True
        ))

        # Join an online game button
        self.gui_container.add(self.create_menu_button(
            y=230,
            text='Join an online game',
            on_click=self.btn_join_online_game_click,
            disabled=True
        ))

        # Host a LAN game button
        self.gui_container.add(self.create_menu_button(
            y=290,
            text='Host a LAN game',
            on_click=self.btn_host_lan_game_click,
            disabled=True
        ))

        # Join a LAN game button
        self.gui_container.add(self.create_menu_button(
            y=340,
            text='Join a LAN game',
            on_click=self.btn_join_lan_game_click,
            disabled=True
        ))

        # Quit button
        self.gui_container.add(self.create_menu_button(
            y=400,
            text='Quit',
            on_click=self.btn_quit_click
        ))

    def draw_title(self):
        title = self.title_font.render('Connect Four', True, settings.COLORS.BLACK.value)
        title_rect = title.get_rect()
        title_rect.centerx = self.app.window.get_rect().centerx
        title_rect.top = 25

        self.app.window.blit(title, title_rect)

        version = self.normal_font.render('v' + settings.VERSION, True, settings.COLORS.BLACK.value)
        version_rect = version.get_rect()
        version_rect.topright = title_rect.bottomright

        self.app.window.blit(version, version_rect)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            gui.event_handler(self.gui_container, event)

        self.app.window.fill(settings.COLORS.WHITE.value)

        self.draw_title()

        self.gui_container.update()
        self.gui_container.draw(self.app.window)
