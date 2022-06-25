#!/usr/bin/env python3

# from modbus_server import ServidorModbus
#
# s = ServidorModbus(12345)
# s.run()
from DataSocket import TCPReceiveSocket, TCPSendSocket, JSON

send_socket = TCPSendSocket(tcp_port=1234, tcp_ip='localhost', send_type=JSON)

while True:
    send_socket.send_data(['T', -100])




