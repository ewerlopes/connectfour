import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, text, text_color, background_color, border_color, border_width=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(rect.size)
        self.rect = rect

        self.image.fill(background_color)

        pygame.draw.rect(self.image, border_color, self.rect, border_width)
