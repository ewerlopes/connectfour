from c4.engine.search.utils import WrongMoveError
from c4.engine.ai.base import Engine


class HumanEngine(Engine):
    def __init__(self, name):
        self.name = name

    def choose(self, board):
        """Ask the user to choose the move"""

        # MOUSE INTERACTIVITY           
        if self.current_player_chip:
            # self.column_change_sound.play()
            mousex, mousey = pygame.mouse.get_pos()
            col_clicked = (mousex / settings.IMAGES_SIDE_SIZE) \
                          % settings.COLS
            if (col_clicked >= 0) and (col_clicked < settings.COLS):
                self.current_player_chip_column = col_clicked
                self.current_player_chip.rect.right = settings.IMAGES_SIDE_SIZE * \
                                                      (self.current_player_chip_column + 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # The user want to go back to the game menu
                    self.app.set_current_screen(menu.Menu, True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # pygame.mouse.get_pressed() returns a tupple 
                # (leftclick, middleclick, rightclick) Each one 
                # is a boolean integer representing button up/down.
                if pygame.mouse.get_pressed()[0]:
                    self._move_chip_down()
        return move

    def __str__(self):
        return self.name
