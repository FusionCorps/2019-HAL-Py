from wpilib import Joystick
from wpilib.buttons import JoystickButton

import robotmap


class XBoxController(Joystick):
    def __init__(self, port: int = robotmap.joystick):
        super().__init__(port)

        buttons = {
            'A': 1,
            'B': 2,
            'X': 3,
            'Y': 4,
            'bumper_l': 5,
            'bumper_r': 6,
            'back': 7,
            'start': 8,
            'stick_l': 9,
            'stick_r': 10
            }

        for button, port in buttons:
            self.__dict__[button] = JoystickButton(self, port)
