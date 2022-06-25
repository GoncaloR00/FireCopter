#!/usr/bin/env python3

import socket
import threading
import pickle

# Parameters for connection
ip_address = socket.gethostname()
port = 2022
# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip_address, port))


# Sending Messages To Server
def write():
    while True:
        try:
            throttle = -100
            yaw = -100
            pitch = -100
            roll = -100
            start = 1
            stop = 1
            sos = 1
            mode = 1
            msg = pickle.dumps((throttle, yaw, pitch, roll, start, stop, sos, mode))
            print(msg)
            print(len(msg))
            client.send(msg)
        except Exception as e:
            print('Error: ', e)
            # TODO meter a acender led de aviso


write_thread = threading.Thread(target=write)
write_thread.start()
