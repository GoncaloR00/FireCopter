#!/usr/bin/env python3
import time
from ControlTower.GamePad.ClassGamePad import ClassGamePad

# -----------------------------------------
# Initialization
# -----------------------------------------

game_pad = ClassGamePad()
game_pad.connect(0)

# -----------------------------------------
# Execution (in cycle)
# -----------------------------------------
while True:

    game_pad.getData()
    print('Axis0=' + str(game_pad.axis0) + '   Axis1=' + str(game_pad.axis1))
    time.sleep(0.01)

# -----------------------------------------
# Termination
# -----------------------------------------
game_pad.stop()
