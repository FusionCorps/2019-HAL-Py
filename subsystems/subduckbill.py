from enum import Enum

from wpilib import Solenoid
from wpilib.command import Subsystem

import robotmap


class StateDuckbill(Enum):
    """
    Duckbill state enum that stores solenoid values in a (bottom, top) format
    """

    HALT = (False, False)
    UP = (True, False)
    DOWN = (False, True)


class SubDuckbill(Subsystem):
    def __init__(self):
        super().__init__("Duckbill")
        self.solenoid_duckbill_B = Solenoid(robotmap.solenoid_piston_B)
        self.solenoid_duckbill_T = Solenoid(robotmap.solenoid_piston_T)
        self.set_state(StateDuckbill.UP)

    def set_state(self, state_target):
        """Sets the state of the Duckbill subsystem using the StateDuckBill Enum.
        Parameters
        ---
        `state_target`: (StateDuckbill) Value to set (e.g. `DOWN`)"""
        if self.solenoid_duckbill_B.get() is not state_target.value[0]:
            self.solenoid_duckbill_B.set(state_target.value[0])
        if self.solenoid_duckbill_T.get() is not state_target.value[1]:
            self.solenoid_duckbill_T.set(state_target.value[1])

        self.state = state_target

    def get_state(self):
        """Returns current StateDuckbill"""
        return self.state

    def initDefaultCommand(self):
        from commands.duckbill.duckbill_set import DuckbillSet

        self.setDefaultCommand(DuckbillSet(StateDuckbill.UP))
