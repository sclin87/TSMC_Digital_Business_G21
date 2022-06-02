import socket
import time
HOST = 'localhost'
PORT = 7878

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    s.send('test'.encode())
    time.sleep(1)