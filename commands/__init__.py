import logging

import oi
from subsystems.duckbill import StateDuckbill
from subsystems.intake import StateIntake
from subsystems.lift import Position
from subsystems.piston import StatePiston

from .duckbill.duckbill_set import DuckbillSet
from .intake.intake_set import IntakeSet
from .lift.lift_drive import LiftDrive
from .lift.lift_grp import LiftGroup
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

    oi.stick_L.whenPressed(IntakeSet(StateIntake.INTAKING))
    oi.stick_L.whenReleased(IntakeSet(StateIntake.HALT))

    oi.stick_R.whenPressed(IntakeSet(StateIntake.SHOOTING))
    oi.stick_R.whenReleased(IntakeSet(StateIntake.HALT))

    oi.back.whenPressed(LiftGroup())

    oi.start.toggleWhenPressed(LiftDrive(0.6, 100))

    # CONTROL MODE 0
    oi.X.whenPressed(LiftSet(Position.BOTH_DOWN))
    oi.B.whenPressed(LiftSet(Position.BOTH_UP))
    oi.A.whenPressed(LiftSet(Position.BOTH_HALT))
    oi.Y.whenPressed(LiftSet(Position.FRONT_UP))

    logger.info("Commands initialized")
