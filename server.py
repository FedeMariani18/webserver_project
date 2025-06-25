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