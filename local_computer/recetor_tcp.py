#!/usr/bin/env python3
from DataSocket import TCPSendSocket, TCPReceiveSocket, JSON
from threading import Thread
import sys

port = 4001
def receiving_function():

    # function to run when a new piece of data is received
    def print_value(data):
        print(data['data'][0])

    rec_socket = TCPReceiveSocket(tcp_port=port, tcp_ip='localhost', handler_function=print_value, as_server=False)
    rec_socket.start(blocking=True)
    while True:
        try:
            pass
        except:
            rec_socket.stop()


if __name__ == '__main__':
    rec_thread = Thread(target=receiving_function)
    rec_thread.start()
    rec_thread.join()
    sys.exit()










