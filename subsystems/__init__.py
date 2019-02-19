import logging

import robotmap

from .chassis import Chassis
from .intake import Intake
from .lift import Lift
from .pneumatics import Pneumatics
from .slapper import Slapper

_chassis, _intake, _pneumatics, _slapper, _lift = None, None, None, None, None


def init():
    """Creates all instances of subsystem classes"""
    logger = logging.getLogger("Subsystems")

    global _chassis, _intake, _pneumatics, _slapper, _lift

    _chassis = Chassis()
    _intake = Intake(robotmap.intake_p, robotmap.intake_i, robotmap.intake_d)
    _pneumatics = Pneumatics()
    _slapper = Slapper()
    _lift = Lift()

    logger.info("Subsystems initialized")
