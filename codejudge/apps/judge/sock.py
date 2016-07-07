import socket
import json

class Socket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        sent = self.sock.send(msg)

sock = Socket()

file = open('1.txt', 'r')
s = file.read()
print s

sock.connect("127.0.0.1", 6029)
d = json.dumps({'id': 6, 
             'filename': "hello.c",
             'code': s,
             'language': "CPP",
             'input': "",
             'output': "Hello World",
             'matchLines': 0,
             'partial': 0,
             'time': 1})
sock.send(d)