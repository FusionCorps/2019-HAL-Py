from wpilib import Joystick
from wpilib.buttons import JoystickButton

import robotmap


class OI():

    def __init__(self):
        self.joystick = Joystick(robotmap.joystick_id)
        self.A = JoystickButton(self.joystick, 1)
        self.B = JoystickButton(self.joystick, 2)
        self.X = JoystickButton(self.joystick, 3)
        self.Y = JoystickButton(self.joystick, 4)
        self.bumper_L = JoystickButton(self.joystick, 5)
        self.bumper_R = JoystickButton(self.joystick, 6)
        self.back = JoystickButton(self.joystick, 7)
        self.start = JoystickButton(self.joystick, 8)
        self.stick_L = JoystickButton(self.joystick, 9)
        self.stick_R = JoystickButton(self.joystick, 10)


oi = OI()
