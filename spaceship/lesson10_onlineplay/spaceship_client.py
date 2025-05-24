import pickle
import socket
from message import *
from network import *
from time import sleep
import queue
import threading

HOST = 'www.tutorcan.com'  # Server address (localhost)
# HOST = "127.0.0.1"
PORT = 65432       # Server port

def talk_to_server(client):
    socket = client.socket
    while True:
        sleep(0.05)
        message_to_send = []
        while not client.send_queue.empty():
            message_to_send.append(client.send_queue.get())
        if len(message_to_send) == 0:
            message_to_send.append(SyncRequest())
        try:
            safe_send(socket, message_to_send)
            resps = safe_recv(socket)
        except:
            pass
        for resp in resps:
            if isinstance(resp, TextResponse):
                print('[Server]', resp.text)
            elif isinstance(resp, SyncResponse):
                client._latest = resp.objs
            elif isinstance(resp, EmptyResponse):
                pass
            else:
                print('Server: unrecognized response ' + resp)

class Client:
    def __init__(self):
        self.send_queue = queue.Queue()
        self.socket = None
        self._latest = {"objects": [], "sounds": []}

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        print("Connected to server")

        threading.Thread(target=talk_to_server, args={self,}, daemon=True).start()
        self.send_queue.put(NewPlayerRequest())

    def move(self, position):
        self.send_queue.put(MoveRequest(position))

    def shoot(self):
        self.send_queue.put(ShootRequest())

    def latest(self):
        return self._latest
