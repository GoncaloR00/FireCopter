#!/usr/bin/env python3
import time
# from ClassGamePad import ClassGamePad
import numpy
import serial
import time

# -----------------------------------------
# Initialization
# -----------------------------------------

# GamePad
# game_pad = ClassGamePad()
# game_pad.connect(0)

# Serial Comunication
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.reset_input_buffer()

# -----------------------------------------
# Execution (in cycle)
# -----------------------------------------
while True:
#     game_pad.getData()
#     yaw_joystick = game_pad.LStickLR
#     throttle_joystick = game_pad.LStickUD
#     roll_joystick = game_pad.RStickLR
#     pitch_joystick = game_pad.RStickUD
#     throttle = numpy.interp(throttle_joystick, [-1, 1], [100, 0])
#     yaw = numpy.interp(yaw_joystick, [-1, 1], [-100, 100])
#     pitch = numpy.interp(pitch_joystick, [-1, 1], [100, -100])
#     roll = numpy.interp(roll_joystick, [-1, 1], [-100, 100])
#     message = str(int(throttle))+',' + str(int(yaw)) + ',' + str(int(pitch)) + ',' + str(int(roll)) + ',' + "\n"
#     ser.write(message.encode('utf-8'))
#     print('Throttle= ' + str(throttle) + ' Yaw= ' + str(yaw) + ' Pitch= ' + str(pitch) + ' Roll =' + str(roll))
    ser.read(10)
    ser.timeout = 0.02
    line = ser.readline().decode('latin-1').rstrip()
    print(line)

# -----------------------------------------
# Termination
# -----------------------------------------
# game_pad.stop()