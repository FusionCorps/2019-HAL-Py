import logging

from .subchassis import SubChassis
from .subduckbill import SubDuckbill
from .subintake import SubIntake
from .sublift import SubLift
from .subpiston import SubPiston

chassis, intake, duckbill, slapper, lift, piston = (
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

    global chassis, intake, duckbill, slapper, lift, piston

    chassis = SubChassis()
    intake = SubIntake()
    duckbill = SubDuckbill()
    lift = SubLift()
    piston = SubPiston()

    logger.info("Subsystems initialized")
