import socket
import threading
import json

def receive_messages(sock):
    pass


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('172.20.10.2', 8080))
    threading.Thread(target=receive_messages, args=(sock,)).start()
    while True:
        message = input()
        payload = {
            "action": "SEND_MESSAGE",
            "data": message
            }
        sock.sendall(json.dumps(payload).encode('utf-8'))
    sock.close()

main()
