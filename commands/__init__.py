import logging

import hal

import robotmap
from inputs import controller
from subsystems.sublift import Position
from .autonomous.profile import ProfileFollower
from .chassis.chassis_drive import ChassisDrive
from .chassis.chassis_swap_mode import ChassisSwapMode
from .duckbill.duckbill_set import DuckbillSet
from .duckbill.duckbill_switch import DuckbillSwitch
from .intake.intake_joystick import IntakeJoystick
from .intake.intake_set import IntakeSet
from .lift.lift_drive import LiftDrive, LiftDrive2
from .lift.lift_grp import ClimbHab2, ClimbHab3
from .lift.lift_reset import LiftReset
from .lift.lift_set import LiftSet
from .piston.piston_grp import PistonGrp
from .piston.piston_set import PistonSet


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    controller.bumper_l.toggleWhenPressed(DuckbillSwitch())
    controller.bumper_r.whenPressed(PistonGrp())
    controller.start.whenPressed(ClimbHab3())
    controller.back.whenPressed(ClimbHab2())
    controller.stick_r.whenPressed(ChassisSwapMode())

    if hal.isSimulation() and robotmap.simulation_lift_target is 0:
        controller.a.whenPressed(LiftSet(Position.FLUSH))
        controller.x.whenPressed(LiftSet(Position.FRONT))
        controller.y.whenPressed(LiftSet(Position.LBACK))
        controller.b.whenPressed(LiftSet(Position.CLIMB))

    if hal.isSimulation() and robotmap.simulation_lift_target is 1:
        controller.a.whenPressed(LiftSet(Position.FLUSH))
        controller.b.whenPressed(LiftSet(Position.CLIMB2))
        controller.x.whenPressed(LiftSet(Position.FRONT2))
        controller.y.whenPressed(LiftSet(Position.LBACK2))

    controller.stick_l.whenPressed(ProfileFollower(file_name="down"))

    # inputs.bumper_L.toggleWhenPressed(LiftReset(0))
    # inputs.bumper_R.toggleWhenPressed(LiftReset(1))

    logger.info("Commands initialized")
