from wpilib import Solenoid
from wpilib.command import Subsystem


class Pneumatics(Subsystem):
    def __init__(self):
        super().__init__("Pneumatics")
    