import pygame

from spaceship import Spaceship, Monster

pygame.init()

window = pygame.display.set_mode((1200, 500))

running = True

spaceship = Spaceship(100,100)

monster001 = Monster(500, 100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill((0, 0, 0))

    spaceship.draw(window)
    monster001.draw(window)

    pygame.display.update()