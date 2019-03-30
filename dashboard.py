from wpilib import SmartDashboard

import robotmap


def init():
    """
    Creates SD objects once at robot start
    """
    SmartDashboard().putNumberArray("Front FPID", robotmap.lift_front_fpid)
    SmartDashboard().putNumberArray("Back FPID", robotmap.lift_back_fpid)


def update():
    """Updates SmartDashboard"""
    robotmap.lift_front_fpid = SmartDashboard().getNumberArray(
        "Front FPID", [0, 0, 0, 0]
    )
    robotmap.lift_back_fpid = SmartDashboard().getNumberArray(
        "Back FPID", [0, 0, 0, 0]
    )
    # pass
