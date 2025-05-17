import pickle
import socket
from message import Text, TextResponse

HOST = '127.0.0.1'  # Server address (localhost)
PORT = 65432       # Server port

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(pickle.dumps([Text('Hello Server')]))
    data = s.recv(32768)

match pickle.loads(data):
    case TextResponse(text=t, owner= _):
        print('Received from server:', t)
    case _:
        print('Received from server: unrecognized response')