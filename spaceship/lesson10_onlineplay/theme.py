import pygame
import os
from world import *
from spaceship import *
from spaceship_client import Client

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
        self.option = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.option == 1 or self.option == 2:
                    Theme.current_theme = MainTheme(self.window, self.font, self.option)
                else:
                    Theme.current_theme = OnlineTheme(self.window, self.font)
            if event.key == pygame.K_DOWN:
                self.option = self.option % 3 + 1

    def update(self):
        self.window.blit(self.title_image, (200, 100))
        # Draw text
        self.window.blit(self.font.render("One Player", 0, (255, 240, 230)), (450, 330))
        self.window.blit(self.font.render("Two Players", 0, (255, 240, 230)), (450, 380))
        self.window.blit(self.font.render("Online Play", 0, (255, 240, 230)), (450, 430))
        # Draw selector
        if self.option == 1:
            pygame.draw.rect(self.window, (255, 240, 230), (400, 330, 15, 15), 0)
            pygame.draw.rect(self.window, (0, 0, 0), (400, 380, 15, 15), 0)
            pygame.draw.rect(self.window, (0, 0, 0), (400, 430, 15, 15), 0)
        elif self.option == 2:
            pygame.draw.rect(self.window, (255, 240, 230), (400, 380, 15, 15), 0)
            pygame.draw.rect(self.window, (0, 0, 0), (400, 330, 15, 15), 0)
            pygame.draw.rect(self.window, (0, 0, 0), (400, 430, 15, 15), 0)
        elif self.option == 3:
            pygame.draw.rect(self.window, (255, 240, 230), (400, 430, 15, 15), 0)
            pygame.draw.rect(self.window, (0, 0, 0), (400, 330, 15, 15), 0)
            pygame.draw.rect(self.window, (0, 0, 0), (400, 380, 15, 15), 0)

        pygame.display.update()

class MainTheme(Theme):
    def __init__(self, window, font, num_player):
        super().__init__(window, font)
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT, self.font)
        self.num_player = num_player
        for i in range(num_player):
            Spaceship(self.world, 99, i * 150 + 100, i)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.world.spaceships[0].move((0, 30))
            if event.key == pygame.K_UP:
                self.world.spaceships[0].move((0, -30))
            if event.key == pygame.K_RIGHT:
                self.world.spaceships[0].shoot()
            if self.num_player == 2:
                if event.key == pygame.K_s:
                    self.world.spaceships[1].move((0, 30))
                if event.key == pygame.K_w:
                    self.world.spaceships[1].move((0, -30))
                if event.key == pygame.K_d:
                    self.world.spaceships[1].shoot()

    def update(self):
        if self.world.gameover:
            Theme.current_theme = GameOverTheme(self.window, self.font)
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.world.spaceships[0].move((0, -1))
        if keys[pygame.K_DOWN]:
            self.world.spaceships[0].move((0, 1))
        if self.num_player == 2:
            if keys[pygame.K_w]:
                self.world.spaceships[1].move((0, -1))
            if keys[pygame.K_s]:
                self.world.spaceships[1].move((0, 1))

        self.world.update()
        self.window.fill((0, 0, 0))
        self.world.draw(self.window)
        pygame.display.update()

class OnlineTheme(Theme):
    def __init__(self, window, font):
        super().__init__(window, font)
        self.world = ClientWorld(1200, 500, self.font)
        self.client = Client()
        self.client.start()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.client.move((0, 30))
            if event.key == pygame.K_UP:
                self.client.move((0, -30))
            if event.key == pygame.K_RIGHT:
                self.client.shoot()

    def update(self):
        if self.world.gameover:
            Theme.current_theme = GameOverTheme(self.window, self.font)
            return

        self.world.load(self.client.latest())
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
