import logging

from wpilib import Solenoid
from wpilib.command import Subsystem

import robotmap


class Pneumatics(Subsystem):
    def __init__(self):
        super().__init__("Pneumatics")
        self.solenoid_venturi_R = Solenoid(robotmap.solenoid_venturi_R)
        self.solenoid_venturi_L = Solenoid(robotmap.solenoid_venturi_L)
        self.solenoid_piston_L = Solenoid(robotmap.solenoid_piston_L)
        self.solenoid_piston_R = Solenoid(robotmap.solenoid_piston_R)

        self.logger = logging.getLogger("Pneumatics")

    def set_venturi(self, state):
        if state == True:
            self.solenoid_venturi_L.set(False)
            self.solenoid_venturi_R.set(True)
        elif state == False:
            self.solenoid_venturi_R.set(False)
            self.solenoid_venturi_L.set(True)

    def set_piston(self, state):
        if state == True:
            self.solenoid_piston_R.set(False)
            self.solenoid_piston_L.set(True)
        elif state == False:
            self.solenoid_piston_L.set(False)
            self.solenoid_piston_R.set(True)

    def set_state(self, target):
        if target == 0:
            self.set_venturi(False)
            self.set_piston(False)
        elif target == 1:
            self.set_venturi(True)
            self.set_piston(False)
        elif target == 2:
            self.set_venturi(False)
            self.set_piston(True)

    def initDefaultCommand(self):
        from commands.pneumatics.halt import Halt

        self.setDefaultCommand(Halt())
