import logging

import oi
from subsystems.duckbill import StateDuckbill
from subsystems.intake import IntakeState
from subsystems.lift import Position
from subsystems.piston import StatePiston

from .autonomous.auto_align import AutoAlign
from .duckbill.duckbill_set import DuckbillSet
from .intake.intake_set import IntakeSet
from .joystick_drive import JoystickDrive
from .lift.backset import BackSet
from .lift.frontset import FrontSet
from .lift.lraise import SetLift
from .piston.piston_set import PistonSet
from .switch_control_mode import SwitchControlMode


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    # CONTROL MODE 1
    oi.bumper_L.toggleWhenPressed(DuckbillSet(StateDuckbill.DOWN))
    oi.bumper_R.toggleWhenPressed(PistonSet(StatePiston.OUT))

    oi.back.whenPressed(SwitchControlMode())

    # CONTROL MODE 2
    oi.B.whenPressed(SetLift(Position.DOWN))
    oi.X.whenPressed(FrontSet(Position.UP))
    oi.Y.whenPressed(BackSet(Position.UP))
    oi.A.whenPressed(SetLift(Position.ZERO))

    # oi.start.toggleWhenPressed(IntakeIntake())

    logger.info("Commands initialized")
