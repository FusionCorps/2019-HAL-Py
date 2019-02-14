import logging

import oi

from .intake.eject import IntakeEject
from .intake.halt import IntakeHalt
from .intake.intake import IntakeIntake
from .intake.shoot import IntakeShoot
from .joystick_drive import JoystickDrive
from .pneumatics.extend import Extend
from .pneumatics.halt import Halt
from .pneumatics.retract import Retract
from .switch_control_mode import SwitchControlMode


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    oi.X.whenPressed(Extend())
    oi.X.whenReleased(Retract())
    oi.A.whenPressed(Halt())
    oi.bumper_L.whenPressed(SwitchControlMode(0))
    oi.bumper_R.whenPressed(SwitchControlMode(1))

    logger.info("Commands initialized")
