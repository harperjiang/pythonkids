

import pickle
import struct

def safe_send(sock, object):
    data = pickle.dumps(object)
    length = struct.pack('>I', len(data))  # 4-byte big-endian length prefix
    sock.sendall(length + data)

def recv_exact(sock, n):
    """Receive exactly n bytes from the socket"""
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise ConnectionError("Socket closed prematurely")
        data.extend(packet)
    return bytes(data)

def safe_recv(sock):
    # First, read the 4-byte length prefix
    raw_len = recv_exact(sock, 4)
    data_len = struct.unpack('>I', raw_len)[0]

    # Then, read the actual data
    data = recv_exact(sock, data_len)
    return pickle.loads(data)

