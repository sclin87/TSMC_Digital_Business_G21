import socket
import time
HOST = 'localhost'
PORT = 7878

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
i = 0
while True:
    print(i)
    s.send("https://taipeitimes.com/News/biz/archives/2022/01/20/2003771688\n".encode('ascii'))
    time.sleep(1)