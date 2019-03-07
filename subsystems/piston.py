import logging
from enum import Enum

from wpilib import Solenoid
from wpilib.command import Subsystem

import robotmap


class StatePiston(Enum):
    """
    Piston state enum that stores tuple with (left, right) values
    """

    HALT = (False, False)
    OUT = (True, False)
    IN = (False, True)


class Piston(Subsystem):
    def __init__(self):
        super().__init__("Piston")
        self.solenoid_piston_L = Solenoid(robotmap.solenoid_piston_L)
        self.solenoid_piston_R = Solenoid(robotmap.solenoid_piston_R)
        self.setState(StatePiston.IN)

    def setState(self, state_target):
        if self.solenoid_piston_L.get() is not state_target[0]:
            self.solenoid_piston_L.set(state_target[0])
        if self.solenoid_piston_R.get() is not state_target[1]:
            self.solenoid_piston_R.set(state_target[1])

    def initDefaultCommand(self):
        pass