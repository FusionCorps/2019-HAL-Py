from wpilib import SmartDashboard

import robotmap
import subsystems


def init():
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
