import os
import pygame

from spaceship import Spaceship
from world import World

pygame.init()
pygame.font.init()

font = pygame.font.Font(os.path.join("res", "fonts", 'PressStart2P-Regular.ttf'), 16)

window = pygame.display.set_mode((1200, 500))

running = True

world = World(1200, 500, font)

spaceship = Spaceship(world, 100,100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                spaceship.move((0, 30))
            if event.key == pygame.K_UP:
                spaceship.move((0, -30))
            if event.key == pygame.K_RIGHT:
                spaceship.shoot()

    world.update()

    window.fill((0, 0, 0))
    world.draw(window)
    pygame.display.update()