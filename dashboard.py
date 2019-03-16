from wpilib import SendableChooser, SmartDashboard
from wpilib.shuffleboard import BuiltInWidgets, Shuffleboard

import robotmap
import subsystems


def init():
    """
    Creates SD objects once at robot start
    """
    SmartDashboard().putNumberArray("Front FPID", subsystems._lift.frontFPID)
    SmartDashboard().putNumberArray("Back FPID", subsystems._lift.backFPID)


def update():
    """Updates SmartDashboard"""
    subsystems._lift.frontFPID = SmartDashboard().getNumberArray(
        "Front FPID", [0, 0, 0, 0]
    )
    subsystems._lift.backFPID = SmartDashboard().getNumberArray(
        "Back FPID", [0, 0, 0, 0]
    )
    # pass
