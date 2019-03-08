from wpilib import SmartDashboard
from wpilib.shuffleboard import BuiltInWidgets, Shuffleboard

import robotmap
import subsystems


def init():
    SmartDashboard().putNumber("CFront Spd", robotmap.spd_lift_cfront)
    SmartDashboard().putNumber("CBack Spd", robotmap.spd_lift_cback)


def update():
    """Sets up SmartDashboard"""
    SmartDashboard().putData("Chassis", subsystems._chassis)
    SmartDashboard().putData("Intake", subsystems._intake)
    SmartDashboard().putNumber("Control Mode", robotmap.control_mode)
    SmartDashboard().putNumber("Slap", robotmap.spd_slapper_slap)
    SmartDashboard().putNumber("Hold", robotmap.spd_slapper_hold)
    # SmartDashboard().putBoolean("Limit Switch", subsystems._slapper.limit_switch.get())
    SmartDashboard().putData("Drive", subsystems._chassis._drive)
