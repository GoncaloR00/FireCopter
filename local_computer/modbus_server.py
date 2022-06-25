#!/usr/bin/env python3

from pyModbusTCP.server import ModbusServer, DataBank
import socket
import random
import time


class ServidorModbus:

    def __init__(self, port):

        self._server = ModbusServer(host=socket.gethostname(), port=port, no_block=True)
        self._db = DataBank()

    def run(self):
        try:
            self._server.start()
            print('Servidor iniciado')
            while True:
                value = random.randrange(int(0.95*400), int(1.05*400))
                self._db.set_words(0, [value])
                print(value)
                print(self._db.get_words(0))
                time.sleep(1)
        except Exception as e:
            print('Erro', e.args)
