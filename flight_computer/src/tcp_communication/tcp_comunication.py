#!/usr/bin/env python3

import socket
import threading
import struct

host = socket.gethostname()
port = 2022
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)