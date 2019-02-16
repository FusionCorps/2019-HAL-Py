from ctre import WPI_TalonSRX
from wpilib import DigitalInput
from wpilib.command import Subsystem

import robotmap
import subsystems


class Slapper(Subsystem):
    def __init__(self):
        super().__init__("Slapper")
        self.slapper = WPI_TalonSRX(robotmap.talon_slapper)
        self.limit_switch = DigitalInput(robotmap.slapper_limit)
