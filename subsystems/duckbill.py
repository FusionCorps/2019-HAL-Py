import logging
from enum import Enum

from wpilib import Solenoid
from wpilib.command import Subsystem

import robotmap


class StateDuckbill(Enum):
    """
    Duckbill state enum that stores tuple with (bottom, top) values
    """

    HALT = (False, False)  # Refrain from using HALT b/c of solenoids
    DOWN = (True, False)
    UP = (False, True)


class Duckbill(Subsystem):
    def __init__(self):
        super().__init__("Duckbill")
        self.solenoid_duckbill_B = Solenoid(robotmap.solenoid_piston_B)
        self.solenoid_duckbill_T = Solenoid(robotmap.solenoid_piston_T)
        self.setState(StateDuckbill.UP)

    def setState(self, state_target):
        if self.solenoid_duckbill_B.get() is not state_target[0]:
            self.solenoid_duckbill_B.set(state_target[0])
        if self.solenoid_duckbill_T.get() is not state_target[1]:
            self.solenoid_duckbill_T.set(state_target[1])

    def initDefaultCommand(self):
        pass
