import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, font, text, text_color, background_color, border_color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(rect.size)
        self.rect = rect
        self.internal_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)

        self.image.fill(background_color)

        pygame.draw.rect(self.image, border_color, self.internal_rect, 1)

        txt = font.render(text, True, text_color)
        txt_rect = txt.get_rect()
        txt_rect.center = self.internal_rect.center

        self.image.blit(txt, txt_rect)
