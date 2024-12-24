import pygame

class Object:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self, dir):
        self.x += dir[0]
        self.y += dir[1]

class Spaceship(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 120, 90)

    def draw(self, window):
        pygame.draw.rect(window, (255, 200, 124), [self.x, self.y, 40, 20], 0) # top wing
        pygame.draw.rect(window, (255, 255, 255), [self.x + 20, self.y + 20, 70, 50], 0) # body
        pygame.draw.rect(window, (255, 200, 124), [self.x, self.y + 70, 40, 20], 0) # bottom wing
        pygame.draw.rect(window, (255, 223, 0), [self.x + 90, self.y + 40, 30, 10], 0) # laser gun


class Bullet(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 5)


class Monster(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), [self.x, self.y, 40, 40], 0)
        pygame.draw.rect(window, (0, 0, 0), [self.x + 4, self.y + 8, 12, 8], 0) # left eye
        pygame.draw.rect(window, (0, 0, 0), [self.x + 24, self.y + 8, 12, 8], 0) # right eye
        pygame.draw.rect(window, (0, 0, 0), [self.x + 4, self.y + 24, 32, 8], 0) # mouth


class RewardItem(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)
