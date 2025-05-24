
class Message:
    def __init__(self, owner):
        self.owner = owner
        pass

class TextRequest(Message):
    def __init__(self, text):
        super().__init__(None)
        self.text = text

class TextResponse(Message):
    def __init__(self, text, owner = None):
        super().__init__(owner)
        self.text = text

class NewPlayerRequest(Message):
    def __init__(self):
        pass

class MoveRequest(Message):
    def __init__(self, direction):
        super().__init__(None)
        self.direction = direction

class ShootRequest(Message):
    def __init__(self):
        super().__init__(None)
        
class EmptyResponse(Message):
    def __init__(self):
        super().__init__(None)

class SyncRequest(Message):
    def __init__(self):
        pass

class SyncResponse(Message):
    def __init__(self, owner, objs):
        super().__init__(owner)
        self.objs = objs
