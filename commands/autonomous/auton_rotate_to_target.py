from networktables import NetworkTables
from wpilib.command import Command

import subsystems


class AutonRotateToTarget(Command):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.requires(subsystems.chassis)
        self.nt = NetworkTables.getTable("limelight")

    def initialize(self):
        self.nt.putNumber("getpipe", 1)

    def execute(self):
        self.tx = self.nt.getNumber("tx", 0)
        self.ty = self.nt.getNumber("ty", 0)
        self.ta = self.nt.getNumber("ta", 0)

        if abs(self.tx) < 1:
            self.end()
        elif self.tx > 1:
            subsystems.chassis._drive.curvatureDrive(0.0, -0.2, True)
        elif self.tx < -1:
            subsystems.chassis._drive.curvatureDrive(0.0, 0.2, True)

    def isFinished(self):
        return abs(self.tx) < 1

    def interrupted(self):
        self.end()

    def end(self):
        subsystems.chassis._drive.curvatureDrive(0.0, 0.0, True)
