
class Message:
    def __init__(self, owner):
        self.owner = owner
        pass

class Text(Message):
    def __init__(self, text):
        super().__init__(None)
        self.text = text

class TextResponse(Message):
    def __init__(self, text, owner):
        super().__init__(owner)
        self.text = text


class NewPlayerMessage(Message):
    def __init__(self):
        pass

class ObjectCreate(Message):
    def __init__(self, object_type, object_id, requester_id, location):
        self.object_type = object_type
        self.object_id = object_id
        self.requester_id = requester_id
        self.location = location

class ObjectRemove(Message):
    def __init__(self, object_id):
        self.object_id = object_id

class ObjectMove(Message):
    def __init__(self, object_id, direction):
        self.object_id = object_id
        self.direction = direction
