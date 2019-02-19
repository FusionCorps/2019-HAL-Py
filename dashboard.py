from wpilib import SmartDashboard
from wpilib.shuffleboard import BuiltInWidgets, Shuffleboard

import robotmap
import subsystems

# def init():
#     Shuffleboard.getTab("Functions").add("Differential").withWidget(
#         BuiltInWidgets.kDifferentialDrive
#     ).withProperties(
#         "Number of wheels", 4, "Wheel diameter", 80, "Show velocity vectors", True
#     ).getEntry()


def update():
    """Sets up SmartDashboard"""
    SmartDashboard().putData("Chassis", subsystems._chassis)
    SmartDashboard().putData("Pneumatics", subsystems._pneumatics)
    SmartDashboard().putData("Intake", subsystems._intake)
    SmartDashboard().putBoolean(
        "Venturi L", subsystems._pneumatics.solenoid_venturi_L.get()
    )
    SmartDashboard().putBoolean(
        "Venturi R", subsystems._pneumatics.solenoid_venturi_R.get()
    )
    SmartDashboard().putBoolean(
        "Piston L", subsystems._pneumatics.solenoid_piston_L.get()
    )
    SmartDashboard().putBoolean(
        "Piston R", subsystems._pneumatics.solenoid_piston_R.get()
    )
    SmartDashboard().putNumber("Control Mode", robotmap.control_mode)
    SmartDashboard().putNumber("Slap", robotmap.spd_slapper_slap)
    SmartDashboard().putNumber("Hold", robotmap.spd_slapper_hold)
    SmartDashboard().putBoolean("Limit Switch", subsystems._slapper.limit_switch.get())
    SmartDashboard().putNumber(
        "Compressor", subsystems._pneumatics.compressor.getPressureSwitchValue()
    )
    SmartDashboard().putData("Drive", subsystems._chassis._drive)
