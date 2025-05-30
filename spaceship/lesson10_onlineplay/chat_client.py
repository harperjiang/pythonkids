import pickle
import socket
import threading
import queue
from time import sleep

from message import *

HOST = 'www.tutorcan.com'  # Server address (localhost)
PORT = 65432       # Server port

send_queue = queue.Queue()

def talk_to_server(socket):
    while True:
        sleep(0.01)
        message_to_send = []
        while not send_queue.empty():
            message_to_send.append(send_queue.get())
        if len(message_to_send) == 0:
            message_to_send.append(SyncRequest())
        try:
            socket.sendall(pickle.dumps(message_to_send))
            data = socket.recv(32768)
            resps = pickle.loads(data)
        except:
            pass
        for resp in resps:
            if isinstance(resp, TextResponse):
                print('[Server]', resp.text)
            elif isinstance(resp, SyncResponse):
                pass
            else:
                print('Server: unrecognized response ' + resp)

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server")

        threading.Thread(target = talk_to_server, args={s,}, daemon=True).start()
        send_queue.put(NewPlayerRequest())

        while True:
            to_send = input("")
            if to_send == "quit" or to_send == "exit":
                exit(0)
            send_queue.put(TextRequest(to_send))
