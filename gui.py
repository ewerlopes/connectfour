import pygame


current_theme = None


class DefaultTheme:
    def __init__(self):
        self.text_color = pygame.Color('black')
        self.text_color_hover = pygame.Color('black')

        self.background_color = pygame.Color('grey')
        self.background_color_hover = pygame.Color('darkgrey')

        self.border_color = pygame.Color('darkgrey')
        self.border_color_hover = pygame.Color('black')

        self.pointer = pygame.cursors.arrow
        self.pointer_hover = pygame.cursors.tri_left

        self.hover_sound = None
        self.click_sound = None


def init(theme=DefaultTheme()):
    global current_theme

    current_theme = theme


def event_handler(gui_container, event):
    global current_theme

    for widget in gui_container:
        if isinstance(widget, Button):
            if widget.on_click is not None and event.type == pygame.MOUSEBUTTONDOWN and widget.rect.collidepoint(event.pos):
                if current_theme.hover_sound:
                    current_theme.hover_sound.stop()
                    current_theme.hover_sound.play()

                widget.on_click()
            elif event.type == pygame.MOUSEMOTION:
                if not widget.is_hovered and widget.rect.collidepoint(event.pos):
                    if current_theme.click_sound:
                        current_theme.click_sound.play()

                    widget.is_hovered = True

                    pygame.mouse.set_cursor(*widget.get_pointer())
                elif widget.is_hovered and not widget.rect.collidepoint(event.pos):
                    widget.is_hovered = False

                    pygame.mouse.set_cursor(*widget.get_pointer())
        elif isinstance(widget, Label):
            if widget.on_click is not None and event.type == pygame.MOUSEBUTTONDOWN and widget.rect.collidepoint(event.pos):
                if current_theme.hover_sound:
                    current_theme.hover_sound.stop()
                    current_theme.hover_sound.play()

                widget.on_click()


class Widget(pygame.sprite.Sprite):
    is_hovered = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def draw(self):
        pass

    def update(self):
        self.draw()

    def get_background_color(self):
        return current_theme.background_color_hover if self.is_hovered else current_theme.background_color

    def get_border_color(self):
        return current_theme.border_color_hover if self.is_hovered else current_theme.border_color

    def get_text_color(self):
        return current_theme.text_color_hover if self.is_hovered else current_theme.text_color

    def get_pointer(self):
        return current_theme.pointer_hover if self.is_hovered else current_theme.pointer


class Label(Widget):
    on_click = None

    def __init__(self, font, text, on_click=None):
        Widget.__init__(self)

        self.font = font
        self.text = text
        self.on_click = on_click

        self.draw()

    def draw(self):
        global current_theme

        self.image = self.font.render(self.text, True, self.get_text_color())
        self.rect = txt.get_rect()


class Button(Widget):
    on_click = None

    def __init__(self, rect, font, text, on_click=None):
        Widget.__init__(self)

        self.image = pygame.Surface(rect.size)
        self.rect = rect
        self.font = font
        self.text = text
        self.internal_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        self.on_click = on_click

        self.draw()

    def draw(self):
        global current_theme

        self.image.fill(self.get_background_color())
        pygame.draw.rect(self.image, self.get_border_color(), self.internal_rect, 1)

        txt = self.font.render(self.text, True, self.get_text_color())
        txt_rect = txt.get_rect()
        txt_rect.center = self.internal_rect.center

        self.image.blit(txt, txt_rect)
