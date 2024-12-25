from spaceship import Object

class World:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        self.objects.remove(obj)

    def draw(self, window):
        for obj in self.objects:
            obj.draw(window)
