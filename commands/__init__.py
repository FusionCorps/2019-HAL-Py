import logging

import oi
from subsystems.subduckbill import StateDuckbill
from subsystems.sublift import Position
from subsystems.subpiston import StatePiston
from .autonomous.auto_profile import AutoProfile
from .chassis.chassis_drive import ChassisDrive
from .duckbill.duckbill_set import DuckbillSet
from .intake.intake_joystick import IntakeJoystick
from .intake.intake_set import IntakeSet
from .lift.lift_drive import LiftDrive, LiftDrive2
from .lift.lift_grp import LiftGroup, LiftGroup2
from .lift.lift_reset import LiftReset
from .lift.lift_set import LiftSet
from .piston.piston_set import PistonSet


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    oi.bumper_L.toggleWhenPressed(DuckbillSet(StateDuckbill.DOWN))

    oi.bumper_R.whenPressed(PistonSet(StatePiston.OUT))
    oi.bumper_R.whenReleased(PistonSet(StatePiston.IN))

    # oi.X.whileHeld(ChassisDrive(0.8, 0.0))
    # oi.stick_L.whenPressed(AutoProfile((1, 0, 0), (-3, 0, 0)))
    # oi.start.whenPressed(LiftGroup())
    # oi.back.whenPressed(LiftGroup2())
    # # oi.stick_L.toggleWhenPressed(LiftDrive(0.5, 1))
    # oi.bumper_L.toggleWhenPressed(LiftReset(0))
    # oi.bumper_R.toggleWhenPressed(LiftReset(1))
    oi.A.whenPressed(LiftSet(Position.FLUSH))
    oi.B.whenPressed(LiftSet(Position.CLIMB2))
    oi.X.whenPressed(LiftSet(Position.FRONT2))
    oi.Y.whenPressed(LiftSet(Position.LBACK2))

    logger.info("Commands initialized")
