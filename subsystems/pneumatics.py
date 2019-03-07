import logging
from enum import Enum

from wpilib import Compressor, Solenoid
from wpilib.command import Subsystem

import robotmap


class DuckbillState(Enum):
    """
    Duckbill state enum that stores tuple with (bottom, top) values
    """

    HALT = (False, False)  # Refrain from using HALT b/c of solenoids
    OUT = (True, False)
    UP = (False, True)


class PistonState(Enum):
    """
    Piston state enum that stores tuple with (left, right) values
    """

    HALT = (False, False)
    OUT = (True, False)
    IN = (False, True)


class Pneumatics(Subsystem):
    def __init__(self):
        super().__init__("Pneumatics")


        
        self.setState(state_duckbill=DuckbillState.HALT, state_piston=PistonState.HALT)
        self.logger = logging.getLogger("Pneumatics")

    def setState(self, state_duckbill=None, state_piston=None):
        if state_duckbill is not None:
            self.setDuckbill(state_duckbill)
        if state_piston is not None:
            self.setPiston(state_piston)

    def setDuckbill(self, state_duckbill):
        if self.solenoid_duckbill_B.get() is not state_duckbill[0]:
            self.solenoid_duckbill_B.set(state_duckbill[0])
        if self.solenoid_duckbill_T.get() is not state_duckbill[1]:
            self.solenoid_duckbill_B.set(state_duckbill[1])

    def setPiston(self, state_pison):
        if self.solenoid_piston_L.get() is not state_pison[0]:
            self.solenoid_piston_L.set(state_pison[0])
        if self.solenoid_piston_R.get() is not state_pison[1]:
            self.solenoid_piston_R.set(state_pison[1])

    def initDefaultCommand(self):
        pass
