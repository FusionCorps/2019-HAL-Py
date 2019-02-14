import logging

from wpilib import Solenoid
from wpilib.command import Subsystem

import robotmap


class Pneumatics(Subsystem):
    def __init__(self):
        super().__init__("Pneumatics")
        self.solenoid_L = Solenoid(robotmap.solenoid_L)
        self.solenoid_R = Solenoid(robotmap.solenoid_R)
        self.logger = logging.getLogger("Pneumatics")

    def extend(self):
        self.logger.info("Extending")
        if self.solenoid_L.get() and not self.solenoid_R.get():
            self.logger.info("LT RF")
            pass
        elif not self.solenoid_L.get() and not self.solenoid_R.get():
            self.logger.info("LF RF")
            self.solenoid_L.set(True)
        elif not self.solenoid_L.get() and self.solenoid_R.get():
            self.logger.info("LF RT")
            self.solenoid_R.set(False)
            self.solenoid_L.set(True)
        elif self.solenoid_L.get() and self.solenoid_R.get():
            self.logger.info("LT RT")
            self.solenoid_R.set(False)

    def retract(self):
        self.logger.info("Retracting")
        if self.solenoid_R.get() and not self.solenoid_L.get():
            self.logger.info("RT LF")
            pass
        elif not self.solenoid_R.get() and not self.solenoid_L.get():
            self.logger.info("RF LF")
            self.solenoid_R.set(True)
        elif not self.solenoid_R.get() and self.solenoid_L.get():
            self.logger.info("RF LT")
            self.solenoid_L.set(False)
            self.solenoid_R.set(True)
        elif self.solenoid_R.get() and self.solenoid_L.get():
            self.logger.info("RT LT")
            self.solenoid_L.set(False)

    def halt(self):
        if self.solenoid_L.get():
            self.logger.info("Halting")
            self.solenoid_L.set(False)
        if self.solenoid_R.get():
            self.logger.info("Halting")
            self.solenoid_R.set(False)

    def initDefaultCommand(self):
        from commands.pneumatics.halt import Halt

        self.setDefaultCommand(Halt())
