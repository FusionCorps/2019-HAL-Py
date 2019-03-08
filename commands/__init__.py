import logging

import oi
from subsystems.duckbill import StateDuckbill
from subsystems.intake import IntakeState
from subsystems.lift import Position
from subsystems.piston import StatePiston

from .duckbill.duckbill_set import DuckbillSet
from .intake.intake_set import IntakeSet
from .lift.lift_set import LiftSet
from .piston.piston_set import PistonSet
from .switch_control_mode import SwitchControlMode


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    # CONTROL MODE 1
    oi.bumper_L.toggleWhenPressed(DuckbillSet(StateDuckbill.DOWN))

    oi.bumper_R.whenPressed(PistonSet(StatePiston.OUT))
    oi.bumper_R.whenReleased(PistonSet(StatePiston.IN))

    oi.stick_L.whenPressed(IntakeSet(IntakeState.INTAKING))
    oi.stick_L.whenReleased(IntakeSet(IntakeState.HALT))

    oi.stick_R.whenPressed(IntakeSet(IntakeState.SHOOTING))
    oi.stick_R.whenReleased(IntakeSet(IntakeState.HALT))

    oi.back.whenPressed(SwitchControlMode())

    # CONTROL MODE 0
    oi.X.whenPressed(LiftSet(Position.BOTH_DOWN))
    oi.B.whenPressed(LiftSet(Position.BOTH_UP))
    oi.A.whenPressed(LiftSet(Position.BOTH_HALT))
    oi.Y.whenPressed(LiftSet(Position.FRONT_UP))

    logger.info("Commands initialized")
