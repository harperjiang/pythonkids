import pygame

class Object:
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.destroyOnBoundary = False
        world.objects.append(self)

    def move(self, direction):
        # if we are going out of the screen, do nothing
        newx = self.x + direction[0]
        newy = self.y + direction[1]
        if not self.world.on_impact(self, (newx, newy, self.width, self.height)):
            self.x += direction[0]
            self.y += direction[1]

    def update(self):
        pass

    def destroy(self, cause):
        self.world.remove(self)

class Spaceship(Object):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 120, 90)

    def draw(self, window):
        pygame.draw.rect(window, (255, 165, 0), [self.x, self.y, 40, 20], 0) # top wing
        pygame.draw.rect(window, (255, 255, 255), [self.x + 20, self.y + 20, 70, 50], 0) # body
        pygame.draw.rect(window, (255, 165, 0), [self.x, self.y + 70, 40, 20], 0) # bottom wing
        pygame.draw.rect(window, (255, 223, 0), [self.x + 90, self.y + 40, 30, 10], 0) # laser gun

    def shoot(self):
        self.world.add(Bullet(self.world, self.x + self.width, self.y + self.height / 2))


class Bullet(Object):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 10, 5)
        self.destroyOnBoundary = True

    def draw(self, window):
        pygame.draw.rect(window, (128, 128, 128), [self.x, self.y, self.width, self.height], 0)

    def update(self):
        self.move((1, 0))

class Monster(Object):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 40, 40)

    def draw(self, window):
        pygame.draw.rect(window, (0, 255, 0), [self.x, self.y, 40, 40], 0)
        pygame.draw.rect(window, (0, 0, 0), [self.x + 4, self.y + 8, 12, 8], 0) # left eye
        pygame.draw.rect(window, (0, 0, 0), [self.x + 24, self.y + 8, 12, 8], 0) # right eye
        pygame.draw.rect(window, (0, 0, 0), [self.x + 4, self.y + 24, 32, 8], 0) # mouth


class RewardItem(Object):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 40, 40)

    def draw(self, window):
        heart_color = (255, 0, 0)
        # pygame.draw.rect(window, heart_color, [self.x, self.y, 40, 40], 0)
        pygame.draw.circle(window, heart_color, (self.x + 10, self.y + 10), 10)
        pygame.draw.circle(window, heart_color, (self.x + 30, self.y + 10), 10)
        # Bottom triangle
        points = [
            (self.x, self.y + 10),  # Left point
            (self.x + self.width // 2, self.y + self.height),  # Bottom point
            (self.x + self.width - 1, self.y + 10)  # Right point
        ]
        pygame.draw.polygon(window, heart_color, points)