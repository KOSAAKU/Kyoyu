import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('172.20.10.2', 8080))

