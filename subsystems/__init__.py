import logging

from .chassis import Chassis

_chassis = None


def init():
    logger = logging.getLogger("Subsystems")
    global _chassis

    _chassis = Chassis()
    logger.info("Subsystems initialized")
