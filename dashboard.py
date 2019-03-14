from wpilib import SmartDashboard
from wpilib.shuffleboard import BuiltInWidgets, Shuffleboard

import robotmap
import subsystems


def init():
    """
    Creates SD objects once at robot start
    """
    SmartDashboard().putNumber("CFront Spd", robotmap.spd_lift_cfront)
    SmartDashboard().putNumber("CBack Spd", robotmap.spd_lift_cback)


def update():
    """Updates SmartDashboard"""
    SmartDashboard().putData("Chassis", subsystems._chassis)
    SmartDashboard().putData("Intake", subsystems._intake)
    SmartDashboard().putNumber("Control Mode", robotmap.control_mode)
    SmartDashboard().putNumber("Slap", robotmap.spd_slapper_slap)
    SmartDashboard().putNumber("Hold", robotmap.spd_slapper_hold)
    SmartDashboard().putNumber(
        "FEncoder", subsystems._lift.talon_drive_CFront.getQuadraturePosition()
    )
    SmartDashboard().putNumber(
        "BEncoder", subsystems._lift.talon_drive_CBack.getQuadraturePosition()
    )
    SmartDashboard().putData("Drive", subsystems._chassis._drive)
