import socket
import threading

def handle_client(conn, addr):
    print('nouvelle connexion')
    allowed_actions = ["SEND_MESSAGE", "REQUEST_SALT", "JOIN_CHANNEL", "CREATE_CHANNEL"]
    while True:
        data = conn.recv(4096)
        if not data:
            break
        print(f"Données reçues : {data}")
        if not data["action"] and data["data"]:
            if data["action"] not in allowed_actions:
                conn.sendall(json.dumps({"action": "ERROR", "data": "Invalid request"}).encode('utf-8'))
                conn.close()
            
        
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