import socket
s = socket.socket()
port = 12345
s.connect(('10.70.7.241', port))
while True:
    print(s.recv(1024).decode())