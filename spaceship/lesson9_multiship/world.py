import random
import time
from spaceship import Monster

class World:
    def __init__(self, width, height, font, num_player):
        self.font = font
        self.objects = []
        self.to_remove = set()
        self.width = width
        self.height = height
        self.start_time = time.time()
        self.last_update = self.start_time
        self.update_interval = 2

        self.gameover = False

        self.spaceships = []
        self.num_player = num_player

    def add(self, obj):
        self.objects.append(obj)
        if type(obj).__name__ == 'Spaceship':
            self.spaceships.append(obj)

    def remove(self, obj):
        self.to_remove.add(obj)

    def visible(self, rect):
        return not (rect[0] < 0 or rect[1] < 0 or rect[0] + rect[2] > self.width or rect[1] + rect[3] > self.height)

    def update(self):
        # Remove obsolete objects
        for obj in self.to_remove:
            self.objects.remove(obj)
        self.to_remove.clear()

        current_time = time.time()
        if current_time - self.last_update > self.update_interval:
            # Generate new monsters every 2 secs
            monster_y = random.randint(50, self.height - 50)
            monster = Monster(self, self.width - 60, monster_y)
            self.last_update = current_time

        # Update existing objects
        for obj in self.objects:
            obj.update()
        self.detect_impact()

    def draw(self, window):
        for obj in self.objects:
            obj.draw(window)
        # Draw the scores
        if self.num_player == 1:
            window.blit(self.font.render("Score: {}".format(self.spaceships[0].score), 0, (255, 240, 230)), (10, 10))
        else:
            window.blit(self.font.render("Player 1 Score: {}, Player 2 Score: {}".format(self.spaceships[0].score, self.spaceships[1].score), 0, (255, 240, 230)), (10, 10))

    def detect_impact(self):
        length = len(self.objects)
        for i in range(length):
            for j in range(i + 1, length):
                obj_i = self.objects[i]
                obj_j = self.objects[j]
                if obj_i.x < obj_j.x + obj_j.width \
                        and obj_i.x + obj_i.width > obj_j.x \
                        and obj_i.y < obj_j.y + obj_j.height \
                        and obj_i.y + obj_i.height > obj_j.y:
                    self.on_object_impact(obj_i, obj_j)

    def on_object_impact(self, obj_i, obj_j):
        if type(obj_i).__name__ == 'Bullet' and type(obj_j).__name__ == 'Bullet':
            obj_j.impact(obj_i)
        else:
            obj_i.impact(obj_j)
            obj_j.impact(obj_i)

    def has_wall_impact(self, obj, new_rect):
        if self.visible(new_rect):
            return False
        return True