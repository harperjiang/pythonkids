import pygame

from spaceship import Spaceship, Monster, RewardItem, Bullet
from world import World

pygame.init()

window = pygame.display.set_mode((1200, 500))

running = True

world = World()

spaceship = Spaceship(100,100)
world.add(spaceship)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                spaceship.move((0, 50))
            if event.key == pygame.K_UP:
                spaceship.move((0, -50))
            if event.key == pygame.K_RIGHT:
                world.add(Bullet(spaceship.x + spaceship.width, spaceship.y + spaceship.height / 2))

    window.fill((0, 0, 0))

    world.draw(window)
    pygame.display.update()