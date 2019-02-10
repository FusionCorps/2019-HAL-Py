from ctre import WPI_TalonSRX
from wpilib.command import Subsystem

import robotmap


class Intake(Subsystem):
    def __init__(self):
        super().__init__("Intake")
        self._talon = WPI_TalonSRX(robotmap.talon_intake)

    def intake(self):
        self._talon.set(robotmap.spd_intake)

    def reverse(self):
        self._talon.set(-robotmap.spd_intake)

    def stop(self):
        self._talon.set(0.0)
