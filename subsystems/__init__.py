import logging

import robotmap

from .chassis import Chassis
from .duckbill import Duckbill
from .intake import Intake
from .lift import Lift
from .piston import Piston

_chassis, _intake, _duckbill, _slapper, _lift, _piston = (
    None,
    None,
    None,
    None,
    None,
    None,
)


def init():
    """Creates all instances of subsystem classes"""
    logger = logging.getLogger("Subsystems")

    global _chassis, _intake, _duckbill, _slapper, _lift, _piston

    _chassis = Chassis()
    _intake = Intake()
    _duckbill = Duckbill()
    _lift = Lift()
    _piston = Piston()

    logger.info("Subsystems initialized")
