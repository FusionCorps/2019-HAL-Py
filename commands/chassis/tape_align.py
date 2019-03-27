from networktables import NetworkTables
from wpilib.command import Command

import subsystems


class TapeAlign(Command):
    def __init__(self):
        super().__init__("TapeAlign")
        self.requires(subsystems.chassis)
        self.nt = NetworkTables.getTable("limelight")
