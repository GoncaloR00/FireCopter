#!/bin/python3

# from pyModbusTCP.client import ModbusClient
#
# client = ModbusClient(host='localhost', port=12345)
#
# client.open()
# # client.write_single_register(0, -100)
# while True:
#     A = client.read_holding_registers(0)
#     print(A)

from pyModbusTCP.server import ModbusServer, DataBank
import socket
import random
import time

server = ModbusServer(host='localhost', port=5000, no_block=True)
db = DataBank()
try:
    server.start()
    if server.open
    db.set_words(0, [15])
    print('Servidor iniciado')
    while True:
        # value = random.randrange(int(0.95*400), int(1.05*400))
        # db.set_words(0, [value])
        # print(value)
        print(db.get_input_registers(0))
        time.sleep(1)
except Exception as e:
    print('Erro', e.args)