import pygame

from spaceship import Spaceship, Monster
from world import World

pygame.init()

window = pygame.display.set_mode((1200, 500))

running = True

world = World(1200, 500)

spaceship = Spaceship(world, 100,100)
monster = Monster(world, 400, 300)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                spaceship.move((0, 20))
            if event.key == pygame.K_UP:
                spaceship.move((0, -20))
            if event.key == pygame.K_RIGHT:
                spaceship.shoot()

    world.update()

    window.fill((0, 0, 0))
    world.draw(window)
    pygame.display.update()