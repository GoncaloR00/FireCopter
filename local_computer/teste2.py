#!/usr/bin/env python3

import struct


teste = struct.pack('!iiii', 1, 2, 3, 4)
print(teste)
# print(teste.decode('utf-8'))