import queue
import socket
import threading
from time import sleep

from message import *
from network import *
from world import *
from spaceship import *

NAMES = {"StoutBog", "WornFlower", "SadDolphin", "SmileHog", "BurnCarrot"}

def handle_client(stub):
    print(f"New connection from {stub.addr}")
    with stub.conn:
        while True:
            try:
                messages = safe_recv(stub.conn)
                for msg in messages:
                    msg.owner = stub.id
                    stub.server.messages.put(msg)
            except:
                print(f"Connection from {stub.addr} closed")
                pass

            resps = []
            while len(resps) == 0:
                while not stub.resp_queue.empty():
                    resps.append(stub.resp_queue.get())
            safe_send(stub.conn, resps)
    stub.close()

def execute_messages(server):
    while True:
        message = server.messages.get()
        (_, sender) = server.clients[message.owner]
        if isinstance(message, NewPlayerRequest):
            print(f"New player {sender.name}")
            server.joingame(sender)
            server.send(TextResponse(f"Welcome, {sender.name}", owner = sender.id))
        elif isinstance(message, TextRequest):
            print(f"{sender.name} said: {message.text}")
            server.send(TextResponse(f"{sender.name} said:{message.text}", owner = None))
        elif isinstance(message, SyncRequest):
            server.send(SyncResponse(owner = sender.id, objs = server.world.dump()))
        elif isinstance(message, MoveRequest):
            server.world.spaceships_by_id[sender.id].move(message.direction)
            server.send(EmptyResponse())
        elif isinstance(message, ShootRequest):
            server.world.spaceships_by_id[sender.id].shoot()
            server.send(EmptyResponse())
        else:
            pass

def update_world(server):
    while server.world is not None:
        world = server.world
        sleep(0.01)
        if world is not None:
            world.update()

class ClientStub:
    def __init__(self, server, conn, addr, resp_queue):
        self.server = server
        self.id = uuid.uuid4()
        self.name = NAMES.pop()
        self.conn = conn
        self.addr = addr
        self.resp_queue = resp_queue

    def close(self):
        self.server.disconnect(self.id)
        NAMES.add(self.name)

class Server:
    def __init__(self):
        self.executor_thread = None
        self.update_world_thread = None
        self.world = None
        self.host = '0.0.0.0'
        self.port = 65432

        self.clients = {}
        self.messages = queue.Queue()

    def start(self):
        self.executor_thread = threading.Thread(target=execute_messages, args=(self,), daemon=True)
        self.executor_thread.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))  # Bind to address
            s.listen()  # Listen for incoming connections
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()

                client_queue = queue.Queue()
                stub = ClientStub(self, conn, addr, client_queue)

                client_thread = threading.Thread(target=handle_client, args=(stub,), daemon=True)
                self.clients[stub.id] = (client_thread, stub)

                client_thread.start()

    def send(self, msg):
        if msg.owner is not None:
            (_, stub) = self.clients[msg.owner]
            stub.resp_queue.put(msg)
        else:
            for (thread, stub) in self.clients.values():
                stub.resp_queue.put(msg)

    def joingame(self, client):
        if self.world is None:
            self.world = ServerWorld(WORLD_WIDTH, WORLD_HEIGHT, None)
            self.update_world_thread = threading.Thread(target=update_world, args=(self,), daemon=True)
            self.update_world_thread.start()
        index = len(self.world.spaceships)
        spaceship = Spaceship(self.world, 99, index * 150 + 100, index)
        spaceship.name = client.name
        self.world.spaceships_by_id[client.id] = spaceship

    def disconnect(self, client_id):
        del self.clients[client_id]
        spaceship = self.world.spaceships_by_id[client_id]
        del self.world.spaceships_by_id[client_id]
        self.world.spaceships.remove(spaceship)
        if len(self.clients) == 0:
            self.world = None

if __name__ == "__main__":
    s = Server()
    s.start()