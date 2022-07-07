#!/usr/bin/env python3

import socket
import threading
import pickle
import time

from ClassGamePad import ClassGamePad
import numpy

# -----------------------------------------
# Commands to send
# -----------------------------------------
# Throttle
# Yaw
# Pitch
# Roll
# Start - Enable Joysticks
# Stop - Disable Joysticks
# Arm - Enable Motors (press 3 seconds)
# SOS - Disable motors (press 3 seconds)
# Mode - Change auto to manual mode and vice-versa

# -----------------------------------------
# Parameters
# -----------------------------------------

# Connection
ip_address = '192.168.0.100'
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
        # Get gamepad data
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
        arm = game_pad.btnX
        stop = game_pad.btnY
        mode = game_pad.btnRB
        # try to send the data
        try:
            # Serialize
            msg = pickle.dumps((throttle, yaw, pitch, roll, start, stop, arm, sos, mode))
            print(msg)
            print(len(msg))
            client.send(msg)
            time.sleep(0.05)
        except Exception as e:
            print('Error: ', e)
            client.close()
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
