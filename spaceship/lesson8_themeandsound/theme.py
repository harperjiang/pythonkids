import pygame
import os
from world import World
from spaceship import Spaceship

class Theme:
    current_theme = None

    def __init__(self, window, font):
        self.window = window
        self.font = font

    def handle_event(self, event):
        pass

    def update(self):
        pass

class StartTheme(Theme):

    def __init__(self, window, font):
        super().__init__(window, font)
        self.title_image = pygame.image.load(os.path.join("res", "images","title.png"))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                Theme.current_theme = MainTheme(self.window, self.font)
                Theme.current_theme.update()

    def update(self):
        self.window.blit(self.title_image, (200, 100))
        self.window.blit(self.font.render("Press Return to start", 0, (255, 240, 230)), (450, 300))
        pygame.display.update()

class MainTheme(Theme):
    def __init__(self, window, font):
        super().__init__(window, font)
        self.world = World(1200, 500, self.font)
        self.spaceship = Spaceship(self.world, 100, 100)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.spaceship.move((0, 30))
            if event.key == pygame.K_UP:
                self.spaceship.move((0, -30))
            if event.key == pygame.K_RIGHT:
                self.spaceship.shoot()

    def update(self):
        if self.world.gameover:
            Theme.current_theme = GameOverTheme(self.window, self.font)
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.spaceship.move((0, -1))
        if keys[pygame.K_DOWN]:
            self.spaceship.move((0, 1))

        self.world.update()
        self.window.fill((0, 0, 0))
        self.world.draw(self.window)
        pygame.display.update()

class GameOverTheme(Theme):
    def __init__(self, window, font):
        super().__init__(window, font)
        self.gameover_image = pygame.image.load(os.path.join("res", "images","gameover.png"))

    def update(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.gameover_image, (300, 100))
        pygame.display.update()
