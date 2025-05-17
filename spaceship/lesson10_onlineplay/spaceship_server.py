import pickle
import queue
import socket
import threading
import uuid
from time import sleep

from message import Text, TextResponse
from world import ServerWorld, World

def handle_client(stub):
    print(f"New connection from {stub.addr}")
    with stub.conn:
        while True:
            data = stub.conn.recv(32768)
            if not data:
                print(f"Connection from {stub.addr} closed")
                break
            messages = pickle.loads(data)
            for msg in messages:
                msg.owner = stub.id
                stub.server.messages.put(msg)

            resp = stub.resp_queue.get()
            stub.conn.sendall(pickle.dumps(resp))
    stub.close()

def execute_messages(server):
    while True:
        sleep(0.2)
        message = server.messages.get()
        match message:
            case Text(text = t):
                server.send(TextResponse(f"Echo:{t}", owner = message.owner))
            case _:
                pass


class ClientStub:
    def __init__(self, server, conn, addr, resp_queue):
        self.server = server
        self.id = uuid.uuid4()
        self.conn = conn
        self.addr = addr
        self.resp_queue = resp_queue

    def close(self):
        del self.server.clients[self.id]

class Server:
    def __init__(self):
        self.executor_thread = None
        self.world = None
        self.host = '127.0.0.1'
        self.port = 65432

        self.clients = {}
        self.messages = queue.Queue()

    def start(self):
        self.executor_thread = threading.Thread(target=execute_messages, args=(self,), daemon=False)
        self.executor_thread.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))  # Bind to address
            s.listen()  # Listen for incoming connections
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()

                client_queue = queue.Queue()
                stub = ClientStub(self, conn, addr, client_queue)

                client_thread = threading.Thread(target=handle_client, args=(stub,), daemon=False)
                self.clients[stub.id] = (client_thread, stub)

                client_thread.start()

    def send(self, msg):
        if msg.owner is not None:
            (_, stub) = self.clients[msg.owner]
            stub.resp_queue.put(msg)
        else:
            for (thread, stub) in self.clients.values():
                stub.resp_queue.put(msg)

if __name__ == "__main__":
    s = Server()
    s.start()