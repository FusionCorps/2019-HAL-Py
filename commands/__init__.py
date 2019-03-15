import logging

import oi
from subsystems.duckbill import StateDuckbill
from subsystems.intake import StateIntake
from subsystems.lift import Position
from subsystems.piston import StatePiston

from .chassis.chassis_drive import ChassisDrive
from .duckbill.duckbill_set import DuckbillSet
from .intake.intake_joystick import IntakeJoystick
from .intake.intake_set import IntakeSet

# from .lift.lift_drive import LiftDrive
# from .lift.lift_grp import LiftGroup
# from .lift.lift_set import LiftSet
from .piston.piston_set import PistonSet
from .switch_control_mode import SwitchControlMode


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    # CONTROL MODE 1
    oi.bumper_L.toggleWhenPressed(DuckbillSet(StateDuckbill.DOWN))

    oi.bumper_R.whenPressed(PistonSet(StatePiston.OUT))
    oi.bumper_R.whenReleased(PistonSet(StatePiston.IN))

    oi.X.whileHeld(ChassisDrive(-0.8, 0.0))
    # oi.B.whenPressed(LiftSet(Position.BOTH_DOWN))
    # oi.A.whenPressed(LiftSet(Position.BOTH_UP))

    logger.info("Commands initialized")
