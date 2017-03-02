import pygame
import config
import game

pygame.init()

pygame.display.set_caption('Connect Four')

clock = pygame.time.Clock()
window = pygame.display.set_mode(config.WINDOW_SIZE)
game = game.Game(window, clock)

while True:
    game.play()
