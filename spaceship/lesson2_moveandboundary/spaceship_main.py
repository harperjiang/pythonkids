import pygame

from spaceship import Spaceship, Monster, RewardItem

pygame.init()

window = pygame.display.set_mode((1200, 500))

running = True

spaceship = Spaceship(100,100)

monster001 = Monster(500, 100)
reward001 = RewardItem(600, 200)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                spaceship.move((0, 50))
            if event.key == pygame.K_UP:
                spaceship.move((0, -50))

    window.fill((0, 0, 0))

    spaceship.draw(window)
    monster001.draw(window)
    reward001.draw(window)

    pygame.display.update()