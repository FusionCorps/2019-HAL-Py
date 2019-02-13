import logging

import robotmap

from .chassis import Chassis
from .intake import Intake
from .pneumatics import Pneumatics

_chassis, _intake, _pneumatics = None, None, None


def init():
    """Creates all instances of subsystem classes"""
    logger = logging.getLogger("Subsystems")

    global _chassis, _intake, _pneumatics

    _chassis = Chassis()
    _intake = Intake(robotmap.intake_p, robotmap.intake_i, robotmap.intake_d)
    _pneumatics = Pneumatics()

    logger.info("Subsystems initialized")
