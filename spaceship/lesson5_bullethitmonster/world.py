
class World:
    def __init__(self, width, height):
        self.objects = []
        self.to_remove = set()
        self.width = width
        self.height = height

    def add(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        self.to_remove.add(obj)

    def visible(self, rect):
        return not (rect[0] < 0 or rect[1] < 0 or rect[0] + rect[2] > self.width or rect[1] + rect[3] > self.height)

    def update(self):
        for obj in self.to_remove:
            self.objects.remove(obj)
        self.to_remove.clear()
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
            obj_j.impact(obj_i)
        else:
            obj_i.impact(obj_j)
            obj_j.impact(obj_i)

    def has_wall_impact(self, obj, new_rect):
        if self.visible(new_rect):
            return False
        return True