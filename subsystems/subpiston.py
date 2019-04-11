from enum import Enum

from wpilib import Solenoid
from wpilib.command import Subsystem

import robotmap


class StatePiston(Enum):
    """Piston state enum that stores tuple with (left, right) values"""

    HALT = (False, False)
    IN = (True, False)
    OUT = (False, True)
    FULL = (True, True)


class SubPiston(Subsystem):
    """Subsystem used to push hatches away from the Duckbill"""

    def __init__(self):
        super().__init__("Piston")
        self._solenoid_l = Solenoid(robotmap.solenoid_piston_l)
        self._solenoid_r = Solenoid(robotmap.solenoid_piston_r)
        self.set_state(StatePiston.IN)

    def set_state(self, state_target: StatePiston):
        """Sets the state of the Piston subsystem using the StatePiston Enum
        Parameters
        ---
        `state_target`: (StatePiston) Value to set (e.g. `OUT`)"""
        if self.get_state().value[0] is not state_target.value[0]:
            self._solenoid_l.set(state_target.value[0])
        if self.get_state().value[1] is not state_target.value[1]:
            self._solenoid_r.set(state_target.value[1])

    def get_state(self) -> StatePiston:
        """Gets the current `StatePiston` of the Piston"""
        for name, value in StatePiston.__members__.items():
            if self._solenoid_l.get() == value.value[0] and self._solenoid_r.get() == value.value[1]:
                return value
        raise LookupError("Could not retrieve Piston State!")

    def initDefaultCommand(self):
        from commands.piston.piston_set import PistonSet

        self.setDefaultCommand(PistonSet(StatePiston.IN))
