import socket
import threading

def handle_client(conn, addr):
    print('nouvelle connexion')
    while True:
        data = conn.recv(4096)
        if not data:
            break
        print(f"Données reçues : {data}")
    conn.close()
    print('connexion fermée')

addr = ("", 8080)
if socket.has_dualstack_ipv6():
    s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
else:
    s = socket.create_server(addr)

print("[serveur] en écoute sur le port 8080...")

while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()