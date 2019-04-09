import logging
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
    """Subsystem used to hold and release hatches"""

    def __init__(self):
        super().__init__("Duckbill")
        self.solenoid_duckbill_B = Solenoid(robotmap.solenoid_piston_b)
        self.solenoid_duckbill_T = Solenoid(robotmap.solenoid_piston_t)
        self.logger = logging.getLogger("Duckbill")
        self.state = None
        self.set_state(StateDuckbill.UP)

    def set_state(self, state_target: StateDuckbill):
        """Sets the state of the Duckbill subsystem using the StateDuckBill Enum.
        Parameters
        ---
        `state_target`: (StateDuckbill) Value to set (e.g. `DOWN`)"""
        if self.solenoid_duckbill_B.get() is not state_target.value[0]:
            self.solenoid_duckbill_B.set(state_target.value[0])
        if self.solenoid_duckbill_T.get() is not state_target.value[1]:
            self.solenoid_duckbill_T.set(state_target.value[1])

        self.state = self.get_state()
        self.logger.warning(f"{self.state.name}")

    def get_state(self) -> StateDuckbill:
        """Returns current StateDuckbill based on solenoid values"""
        for name, value in StateDuckbill.__members__.items():
            if self.solenoid_duckbill_B.get() == value.value[0] and self.solenoid_duckbill_T.get() == value.value[1]:
                return value
        raise LookupError

    def initDefaultCommand(self):
        pass
