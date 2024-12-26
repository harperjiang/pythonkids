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

    def draw(self, window):
        for obj in self.objects:
            obj.draw(window)
