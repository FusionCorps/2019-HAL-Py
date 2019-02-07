from wpilib import SmartDashboard

import subsystems


def init():
    """Sets up SmartDashboard"""
    SmartDashboard().putData('Chassis', subsystems._chassis)
