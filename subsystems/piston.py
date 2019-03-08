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
    IN = (True, False)
    OUT = (False, True)


class Piston(Subsystem):
    def __init__(self):
        super().__init__("Piston")
        self.solenoid_piston_L = Solenoid(robotmap.solenoid_piston_L)
        self.solenoid_piston_R = Solenoid(robotmap.solenoid_piston_R)
        self.setState(StatePiston.IN)

    def setState(self, state_target):
        """
        Sets the state of the Piston subsystem using the StatePiston Enum.

        `state_target` is the StatePiston Enum value to set (e.g. `OUT`)
        """
        if self.solenoid_piston_L.get() is not state_target.value[0]:
            self.solenoid_piston_L.set(state_target.value[0])
        if self.solenoid_piston_R.get() is not state_target.value[1]:
            self.solenoid_piston_R.set(state_target.value[1])

        self.state = state_target

    def getState(self):
        return self.state

    def initDefaultCommand(self):
        from commands.piston.piston_set import PistonSet

        self.setDefaultCommand(PistonSet(StatePiston.IN))
