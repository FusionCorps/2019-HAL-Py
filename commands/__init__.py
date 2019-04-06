import logging

import hal

import oi
import robotmap
from subsystems.sublift import Position
from .autonomous.profile import ProfileFollower
from .chassis.chassis_drive import ChassisDrive
from .chassis.chassis_set_mode import ChassisSetMode
from .duckbill.duckbill_set import DuckbillSet
from .duckbill.duckbill_switch import DuckbillSwitch
from .intake.intake_joystick import IntakeJoystick
from .intake.intake_set import IntakeSet
from .lift.lift_drive import LiftDrive, LiftDrive2
from .lift.lift_grp import LiftGroup, LiftGroup2
from .lift.lift_reset import LiftReset
from .lift.lift_set import LiftSet
from .piston.piston_grp import PistonGrp
from .piston.piston_set import PistonSet


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    oi.bumper_L.toggleWhenPressed(DuckbillSwitch())
    oi.bumper_R.whenPressed(PistonGrp())
    oi.start.whenPressed(LiftGroup())
    oi.back.whenPressed(LiftGroup2())
    oi.stick_R.whenPressed(ChassisSetMode())

    if hal.isSimulation() and robotmap.simulation_lift_target is 0:
        oi.A.whenPressed(LiftSet(Position.FLUSH))
        oi.X.whenPressed(LiftSet(Position.FRONT))
        oi.Y.whenPressed(LiftSet(Position.LBACK))
        oi.B.whenPressed(LiftSet(Position.CLIMB))

    if hal.isSimulation() and robotmap.simulation_lift_target is 1:
        oi.A.whenPressed(LiftSet(Position.FLUSH))
        oi.B.whenPressed(LiftSet(Position.CLIMB2))
        oi.X.whenPressed(LiftSet(Position.FRONT2))
        oi.Y.whenPressed(LiftSet(Position.LBACK2))

    # oi.bumper_L.toggleWhenPressed(DuckbillSet(StateDuckbill.DOWN))
    # oi.bumper_R.whenReleased(PistonSet(StatePiston.IN))

    # oi.bumper_L.toggleWhenPressed(LiftReset(0))
    # oi.bumper_R.toggleWhenPressed(LiftReset(1))

    # oi.stick_L.whenPressed(
    #     # ProfileFollower(file_loc="/home/lvuser/py/commands/autonomous/", name="diagonal"))
    #     ProfileFollower(file_loc="C:/Users/winst/Documents/Code/2019-Hal-Py/commands/autonomous/", file_name="huge"))

    # oi.stick_R.whenPressed(ProfileFollower((1, 0, 0), (2, 0, 0), (5, 5, 45), name="tiny",
    #                                        file_loc="C:/Users/winst/Documents/Code/2019-Hal-Py/commands/autonomous/",
    #                                        file_name="tiny", generate=True))

    # # oi.X.whileHeld(ChassisDrive(0.8, 0.0))
    # oi.stick_L.whenPressed(AutoProfile((1, 0, 0), (3, 0, 0)))
    # # oi.stick_L.toggleWhenPressed(LiftDrive(0.5, 1))

    logger.info("Commands initialized")
