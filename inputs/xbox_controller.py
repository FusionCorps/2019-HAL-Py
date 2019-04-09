from wpilib import Joystick
from wpilib.buttons import JoystickButton

import robotmap


class XBoxController(Joystick):
    def __init__(self, port: int = robotmap.joystick):
        super().__init__(port)

        buttons = {
            'a': 1,
            'b': 2,
            'x': 3,
            'y': 4,
            'bumper_l': 5,
            'bumper_r': 6,
            'back': 7,
            'start': 8,
            'stick_l': 9,
            'stick_r': 10
            }

        for button, number in buttons.items():
            self.__dict__[str(button)] = JoystickButton(self, number)
