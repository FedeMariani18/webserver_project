import socket
import os
from datetime import datetime

# Server configuration
HOST = '127.0.0.1'
PORT = 8080
WEB_ROOT = 'www' # Directory where web files are stored

# Supported MIME types for different file extensions
MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    '.ico': 'image/x-icon'
}

def get_mime_type(file_path):
    # Get the file extension and return the corresponding MIME type
    ext = os.path.splitext(file_path)[1]
    return MIME_TYPES.get(ext, 'application/octet-stream')

def log_request(method, path, status):
    # Print a log of the HTTP request with timestamp, method, path, and status code
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {method} {path} -> {status}")

def handle_request(client_socket):
    # Receive the HTTP request from the client
    request = client_socket.recv(1024).decode()
    lines = request.splitlines()
    
    if not lines:
        # If the request is empty, close the connection
        client_socket.close()
        return

    # Parse the HTTP method and path from the first request line
    method, path, _ = lines[0].split()

    if method != 'GET':
         # Only GET requests are supported; respond with 405 for others
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        client_socket.send(response.encode())
        client_socket.close()
        return

    if path == '/':
        # Default to index.html if root is requested
        path = '/index.html'

    # Build the full file path
    file_path = os.path.join(WEB_ROOT, path.strip('/'))

    if os.path.isfile(file_path):
        # If the file exists, read and send its contents
        with open(file_path, 'rb') as f:
            content = f.read()
        mime_type = get_mime_type(file_path)
        # Send HTTP 200 OK response with the correct Content-Type
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\n\r\n"
        client_socket.send(response.encode() + content)
        log_request(method, path, 200)
    else:
        # If the file does not exist, send a 404 Not Found response
        response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 - File Not Found</h1>"
        client_socket.send(response.encode())
        log_request(method, path, 404)

    # Close the client connection
    client_socket.close()

def run_server():
    # Create a TCP socket and bind it to the specified host and port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(5) # Listen for incoming connections (max 5 in queue)
        print(f"Server in ascolto su http://{HOST}:{PORT}")

        # Main loop to accept and handle client requests
        while True:
            # Accept a new client connection
            client_socket, _ = server.accept()
            handle_request(client_socket) # Handle the client's HTTP request

if __name__ == "__main__":
    # Start the server if this script is run directly
    run_server()