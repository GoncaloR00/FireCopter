import pygame
from ClassAbstractHardware import ClassAbstractHardware


class ClassGamePad(ClassAbstractHardware):

    def __init__(self):
        super().__init__()
        self.LStickLR = None
        self.LStickUD = None
        self.RStickLR = None
        self.RStickUD = None
        self.LTrigger = None
        self.RTrigger = None
        self.btnA = None
        self.btnB = None
        self.btnX = None
        self.btnY = None
        self.btnLB = None
        self.btnRB = None
        self.btnDP_L = None
        self.btnDP_R = None
        self.btnDP_U = None
        self.btnDP_D = None

    def _connect(self, device):
        pygame.init()
        pygame.joystick.init()  # Initialize the joysticks.

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()
        print('Found ' + str(joystick_count) + ' joysticks.')
        if joystick_count < 1:
            print('No joysticks found. Cannot connect!')
            return False

        # init joystick
        self.joystick = pygame.joystick.Joystick(device)
        self.joystick.init()

        # Get the name from the OS for the controller/joystick.
        joystick_name = self.joystick.get_name()
        print('Connected to ' + joystick_name)

        number_axes = self.joystick.get_numaxes()
        return True

    def _disconnect(self):
        pygame.quit()
        return True

    def _getData(self):
        self.LStickLR = self.joystick.get_axis(0)  # Left stick - left and right
        self.LStickUD = self.joystick.get_axis(1)  # Left stick - up and down
        self.RStickLR = self.joystick.get_axis(3)  # Right stick - left and right
        self.RStickUD = self.joystick.get_axis(4)  # Right stick - up and down
        self.LTrigger = self.joystick.get_axis(2)  # Left trigger
        self.RTrigger = self.joystick.get_axis(5)  # Right trigger
        self.btnA = self.joystick.get_button(0)    # Button A
        self.btnB = self.joystick.get_button(1)    # Button B
        self.btnX = self.joystick.get_button(2)  # Button X
        self.btnY = self.joystick.get_button(3)  # Button Y
        self.btnLB = self.joystick.get_button(4)  # Button Left bumper
        self.btnRB = self.joystick.get_button(5)  # Button Right bumper
        self.btnDP_L = self.joystick.get_button(11)  # Button D-Pad Left
        self.btnDP_R = self.joystick.get_button(12)  # Button D-Pad Right
        self.btnDP_U = self.joystick.get_button(13)  # Button D-Pad Up
        self.btnDP_D = self.joystick.get_button(14)  # Button D-Pad Down

        pygame.event.pump()
        return True

    def _setData(self):
        print('Cannot write anything to camera!')
        return False
