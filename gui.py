import pygame


def event_handler(gui_group, event):
    for widget in gui_group:
        if isinstance(widget, Button):
            if widget.on_click is not None and event.type == pygame.MOUSEBUTTONDOWN and widget.rect.collidepoint(event.pos):
                widget.on_click()
            elif event.type == pygame.MOUSEMOTION:
                if not widget.is_hovered and widget.rect.collidepoint(event.pos):
                    widget.is_hovered = True
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                elif widget.is_hovered and not widget.rect.collidepoint(event.pos):
                    widget.is_hovered = False
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)


class Widget(pygame.sprite.Sprite):
    is_hovered = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def draw(self):
        pass


class Button(Widget):
    on_click = None

    def __init__(self, rect, font, text, text_color, background_color, border_color, border_color_hover, on_click=None):
        Widget.__init__(self)

        self.image = pygame.Surface(rect.size)
        self.rect = rect
        self.font = font
        self.text = text
        self.text_color = text_color
        self.background_color = background_color
        self.border_color = border_color
        self.border_color_hover = border_color_hover
        self.internal_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        self.on_click = on_click

        self.draw()

    def draw(self):
        self.image.fill(self.background_color)

        pygame.draw.rect(self.image, self.border_color_hover if self.is_hovered else self.border_color, self.internal_rect, 2)

        txt = self.font.render(self.text, True, self.text_color)
        txt_rect = txt.get_rect()
        txt_rect.center = self.internal_rect.center

        self.image.blit(txt, txt_rect)

    def update(self):
        self.draw()
