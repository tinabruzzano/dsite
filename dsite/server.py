# dsite/server.py

import socket
from dsite.http.request import Request
from dsite.urls import urlpatterns


def resolve(path):
    for route, view in urlpatterns:
        if route == path:
            return view
    return None


def handle(client):
    raw = client.recv(4096).decode()

    if not raw:
        return

    parts = raw.split("\r\n")

    method, full_path, _ = parts[0].split()

    headers = {}
    i = 1

    while parts[i] != "":
        k, v = parts[i].split(": ", 1)
        headers[k] = v
        i += 1

    body = parts[-1] if parts[-1] else ""

    request = Request(method, full_path, headers, body)

    path = full_path.split("?")[0]

    view = resolve(path)

    if view:
        response = view(request)
        client.send(response.to_http().encode())
    else:
        client.send(b"HTTP/1.1 404 Not Found\r\n\r\n404 Not Found")

    client.close()


def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8000))
    server.listen(5)

    print("[DSite] Server attivo su http://127.0.0.1:8000")

    while True:
        client, addr = server.accept()
        handle(client)
