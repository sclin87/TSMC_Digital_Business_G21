import socket

HOST = '140.113.68.204'
PORT = 7878



testcases = [
    "2022-03-04 https://www.koreatimes.co.kr/www/tech/2022/05/419_329740.html\n", # pass
    "20220304 https://www.koreatimes.co.kr/www/tech/2022/05/419_329740.html\n", # fail : Date wrong format
    "2022-03-32 https://www.koreatimes.co.kr/www/tech/2022/05/419_329740.html\n", # fail : Date wrong format
    "https://www.koreatimes.co.kr/www/tech/2022/05/419_329740.html\n 2022-03-04\n", # fail
    "2022/03/04 https://www.koreatimes.co.kr/www/tech/2022/05/419_329740.html\n", # fail
    "2020-02-28     https://www.koreatimes.co.kr/www/tech/2022/05/419_329740.html\n", # pass
    "2020-02-29     https://www.koreatimes.co.kr/www/tech/2022/05/419_329740.html\n", # fail
    "2022-03-04\nhttps://www.koreatimes.co.kr/www/tech/2022/05/419_329740.html\n", # pass
    "111-03-04 https://www.koreatimes.co.kr/www/tech/2022/05/419_329740.html\n", # fail
    "https://www.koreatimes.co.kr/www/tech/2022/05/419_329740.html\n", # fail
    "2022-03-04 flkjw;fkej;welkfje;fkejkej\n"
]

for i,testcase in enumerate(testcases):
    print("Case {}:".format(i))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    outdata = testcase
    print('send: ' + outdata, end='')
    s.send(outdata.encode('ascii'))
    
    indata = s.recv(1024)
    if len(indata) == 0: # connection closed
        s.close()
        print('server closed connection.')
        break
    print('recv: ' + indata.decode('ascii') + '\n')