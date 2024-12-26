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
        self.to_remove = []
        self.width = width
        self.height = height

    def add(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        self.to_remove.append(obj)

    def visible(self, rect):
        return not (rect[0] < 0 or rect[1] < 0 or rect[0] + rect[2] > self.width or rect[1] + rect[3] > self.height)

    def update(self):
        for obj in self.to_remove:
            self.objects.remove(obj)
        self.to_remove = []
        for obj in self.objects:
            obj.update()
        self.detect_impact(when_impact)

    def draw(self, window):
        for obj in self.objects:
            obj.draw(window)

    def detect_impact(self, callback):
        length = len(self.objects)
        for i in range(length):
            for j in range(i + 1, length):
                obj_i = self.objects[i]
                obj_j = self.objects[j]
                if obj_i.x < obj_j.x + obj_j.width \
                    and obj_i.x + obj_i.width > obj_j.x \
                    and obj_i.y < obj_j.y + obj_j.height \
                    and obj_i.y + obj_i.height > obj_j.y:
                    callback(obj_i, obj_j)

