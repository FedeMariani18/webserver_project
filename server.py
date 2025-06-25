import socket
import os
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8080
WEB_ROOT = 'www'

MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    '.ico': 'image/x-icon'
}

def get_mime_type(file_path):
    ext = os.path.splitext(file_path)[1]
    return MIME_TYPES.get(ext, 'application/octet-stream')

def log_request(method, path, status):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {method} {path} -> {status}")

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    lines = request.splitlines()
    print(lines)
    
    if not lines:
        client_socket.close()
        return

    method, path, _ = lines[0].split()

    if method != 'GET':
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        client_socket.send(response.encode())
        client_socket.close()
        return

    if path == '/':
        path = '/index.html'

    file_path = os.path.join(WEB_ROOT, path.strip('/'))

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        mime_type = get_mime_type(file_path)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\n\r\n"
        client_socket.send(response.encode() + content)
        log_request(method, path, 200)
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 - File Not Found</h1>"
        client_socket.send(response.encode())
        log_request(method, path, 404)

    client_socket.close()