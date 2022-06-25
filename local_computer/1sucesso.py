#!/usr/bin/env python3

from DataSocket import TCPSendSocket, TCPReceiveSocket, JSON
from threading import Thread
import sys

port = 4001  # TCP port to use


# define a function to send data across a TCP socket
def sending_function():
    send_socket = TCPSendSocket(tcp_port=port, tcp_ip='localhost', send_type=JSON, verbose=False, as_server=True, include_time=True)
    send_socket.start(blocking=True)

    while True:
        send_socket.send_data((1, 2, 3, 4))

    # send_socket.stop()


# define a function to receive and print data from a TCP socket
def receiving_function():

    # function to run when a new piece of data is received
    def print_value(data):
        print(data['data'])

    rec_socket = TCPReceiveSocket(tcp_port=port, tcp_ip='localhost', handler_function=print_value, as_server=False)
    rec_socket.start(blocking=True)
    while True:
        try:
            pass
        except:
            rec_socket.stop()


if __name__ == '__main__':
    # define separate threads to run the sockets simultaneously
    send_thread = Thread(target=sending_function)
    # rec_thread1 = Thread(target=receiving_function)
    # rec_thread2 = Thread(target=receiving_function)

    # rec_thread1.start()
    # rec_thread2.start()
    send_thread.start()

    send_thread.join()
    # rec_thread1.join()
    # rec_thread2.join()

    sys.exit()