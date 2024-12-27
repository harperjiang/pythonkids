import random
import time
from spaceship import Monster

def when_impact(obj_i, obj_j):
    world = obj_i.world
    if type(obj_i).__name__ == 'Bullet' and type(obj_j).__name__ == 'Bullet':
        world.remove(obj_j)
    elif type(obj_i).__name__ == 'Bullet' and type(obj_j).__name__ == 'Monster' or \
        type(obj_j).__name__ == 'Bullet' and type(obj_i).__name__ == 'Monster':
        world.remove(obj_i)
        world.remove(obj_j)


class World:
    def __init__(self, width, height):
        self.objects = []
        self.to_remove = set()
        self.width = width
        self.height = height
        self.start_time = time.time()
        self.last_update = self.start_time
        self.update_interval = 2

    def add(self, obj):
        self.objects.append(obj)

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
            obj_j.destroy(obj_i)
        elif type(obj_i).__name__ == 'Bullet' and type(obj_j).__name__ == 'Monster' or \
                type(obj_j).__name__ == 'Bullet' and type(obj_i).__name__ == 'Monster':
            obj_i.destroy(obj_j)
            obj_j.destroy(obj_i)

    def on_impact(self, obj, new_rect):
        if self.visible(new_rect):
            return False
        if type(obj).__name__ == 'Bullet':
            obj.destroy(self)
            return False
        return True