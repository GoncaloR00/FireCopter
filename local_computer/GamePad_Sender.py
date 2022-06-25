#!/usr/bin/env python3

import socket
import threading
import pickle
import time

from ClassGamePad import ClassGamePad
import numpy


# -----------------------------------------
# Parameters
# -----------------------------------------

# Connection
ip_address = '192.168.1.213'
port = 2022


# -----------------------------------------
# Initialization
# -----------------------------------------

# GamePad
game_pad = ClassGamePad()
game_pad.connect(0)

# Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip_address, port))


# Sending Messages To Server
def write():
    while True:
        game_pad.getData()
        yaw_joystick = game_pad.LStickLR
        throttle_joystick = game_pad.LStickUD
        roll_joystick = game_pad.RStickLR
        pitch_joystick = game_pad.RStickUD
        throttle = round(numpy.interp(throttle_joystick, [-1, 1], [100, 0]))
        yaw = round(numpy.interp(yaw_joystick, [-1, 1], [-100, 100]))
        pitch = round(numpy.interp(pitch_joystick, [-1, 1], [100, -100]))
        roll = round(numpy.interp(roll_joystick, [-1, 1], [-100, 100]))
        print(type(roll))
        start = game_pad.btnA
        sos = game_pad.btnB
        stop = game_pad.btnY
        mode = game_pad.btnRB
        try:
            msg = pickle.dumps((throttle, yaw, pitch, roll, start, stop, sos, mode))
            print(msg)
            print(len(msg))
            client.send(msg)
            time.sleep(0.05)
        except Exception as e:
            print('Error: ', e)
            client.close()
            # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip_address, port))


# -----------------------------------------
# Execution
# -----------------------------------------
write_thread = threading.Thread(target=write)
write_thread.start()

# -----------------------------------------
# Termination
# -----------------------------------------
# game_pad.stop()
