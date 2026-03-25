import socket
import threading
import json
groups = {}

def get_group(conn):
    for group in groups.values():
        if conn in group["clients"]:
            return group
    return None

def handle_client(conn, addr):
    print(f'[DEBUG] nouvelle connexion : {conn}')
    allowed_actions = ["SEND_MESSAGE", "REQUEST_SALT", "JOIN_CHANNEL", "CREATE_CHANNEL"]
    while True:
        data = conn.recv(4096)
        data = json.loads(data.decode('utf-8'))
        print(f"Groups : {groups}")
        if not data:
            break
        print(f"[DEBUG] Données reçues : {data}")

        if not data["action"] and data["data"]:
            if data["action"] not in allowed_actions:
                conn.sendall(json.dumps({"action": "ERROR", "data": "Invalid request"}).encode('utf-8'))
                conn.close()

        if data["action"] == "SEND_MESSAGE":
            group = get_group(conn)
            if group is None:
                conn.sendall(json.dumps({"action": "ERROR", "data": "You are not in a group"}).encode('utf-8'))
                conn.close()
                return

            for client in group["clients"]:
                if client != conn:
                    client.sendall(json.dumps({"action": "SEND_MESSAGE", "data": data["data"]}).encode('utf-8'))

            
        elif data["action"] == "REQUEST_SALT":
            # check if data contain {uid}
            if "uid" not in data:
                conn.sendall(json.dumps({"action": "ERROR", "data": "Invalid request"}).encode('utf-8'))
                conn.close()
            
            # check if uid exist
            if data["uid"] not in groups:
                conn.sendall(json.dumps({"action": "ERROR", "data": "UID not found"}).encode('utf-8'))
                conn.close()

            # send salt
            conn.sendall(json.dumps({"action": "REQUEST_SALT", "data": groups[data["uid"]]["salt"]}).encode('utf-8'))
        elif data["action"] == "JOIN_CHANNEL":
            # check if data contain {salt, uid}
            if "salt" not in data or "uid" not in data:
                conn.sendall(json.dumps({"action": "ERROR", "data": "Invalid request"}).encode('utf-8'))
                conn.close()
            
            # check if uid exist
            if data["uid"] not in groups:
                conn.sendall(json.dumps({"action": "ERROR", "data": "UID not found"}).encode('utf-8'))
                conn.close()
            
            # check if salt match
            if data["salt"] != groups[data["uid"]]["salt"]:
                conn.sendall(json.dumps({"action": "ERROR", "data": "Invalid salt"}).encode('utf-8'))
                conn.close()
            
            # add client to group
            groups[data["uid"]]["clients"].append(conn)
        elif data["action"] == "CREATE_CHANNEL":
            # check if data contain {salt, uid}
            if "salt" not in data or "uid" not in data:
                conn.sendall(json.dumps({"action": "ERROR", "data": "Invalid request"}).encode('utf-8'))
                conn.close()
            
            # check if uid already exist
            if data["uid"] in groups:
                conn.sendall(json.dumps({"action": "ERROR", "data": "UID already exist"}).encode('utf-8'))
                conn.close()
            
            # create group
            groups[data["uid"]] = {"clients": [conn], "salt": data["salt"]}
        else:
            conn.sendall(json.dumps({"action": "ERROR", "data": "Invalid request"}).encode('utf-8'))
            conn.close()

    conn.close()
    for group in groups.values():
        if conn in group["clients"]:
            group["clients"].remove(conn)
            if len(group["clients"]) == 0:
                del groups[group["uid"]]
            break
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