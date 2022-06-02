import socket

HOST = '0.0.0.0'
PORT = 7878

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)

while True:
    print('Listening at %s:%d' % (HOST, PORT))
    conn, addr = sock.accept()
    print('Connection from %s:%d' % (addr[0], addr[1]))
    data = ''

    while True:
        indata = conn.recv(1024)
        data += indata.decode('ascii')
        if data[-1] == '\n':
            data = data[:-1]
            break
    
    print('-', data)
    conn.close()
