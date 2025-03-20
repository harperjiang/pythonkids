import os
import pygame

from spaceship import Spaceship
from world import World
from theme import Theme, StartTheme

pygame.init()
pygame.font.init()

font = pygame.font.Font(os.path.join("res", "fonts", 'PressStart2P-Regular.ttf'), 16)

window = pygame.display.set_mode((1200, 500))

running = True

pygame.mixer.music.load(os.path.join("res", "sounds", "theme.wav"))
pygame.mixer.music.play(-1)

Theme.current_theme = StartTheme(window, font)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        Theme.current_theme.handle_event(event)

    Theme.current_theme.update()
