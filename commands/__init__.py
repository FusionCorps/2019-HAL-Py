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
# from .lift.lift_reset import LiftReset
from .lift.lift_set import LiftSet
from .piston.piston_set import PistonSet
from .switch_control_mode import SwitchControlMode


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    oi.bumper_L.toggleWhenPressed(DuckbillSet(StateDuckbill.DOWN))

    oi.bumper_R.whenPressed(PistonSet(StatePiston.OUT))
    oi.bumper_R.whenReleased(PistonSet(StatePiston.IN))

    # oi.X.whileHeld(ChassisDrive(0.8, 0.0))
    # oi.Y.whenPressed(AutoProfile((1, 0, 0), (3, 0, 0)))
    oi.A.whenPressed(LiftSet(Position.BOTH_UP))
    oi.B.whenPressed(LiftSet(Position.BOTH_DOWN))
    oi.X.whenPressed(LiftSet(Position.FRONT_DOWN))
    oi.Y.whenPressed(LiftSet(Position.BACK_DOWN))

    logger.info("Commands initialized")
