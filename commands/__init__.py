import logging

import oi

from .autonomous.auto_align import AutoAlign
from .intake.eject import IntakeEject
from .intake.halt import IntakeHalt
from .intake.intake import IntakeIntake
from .intake.shoot import IntakeShoot
from .joystick_drive import JoystickDrive
from .lift.backset import BackSet
from .lift.frontset import FrontSet
from .lift.lraise import SetLift
from .pneumatics.close import PneumaticsClose
from .pneumatics.piston import PneumaticsPiston
from .pneumatics.venturi import PneumaticsVenturi
from .slapper.hold import SlapperHold
from .slapper.hover import SlapperHover
from .slapper.slap import SlapperSlap
from .slapper.sraise import SlapperRaise
from .slapper.stop import SlapperStop
from .switch_control_mode import SwitchControlMode


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    oi.bumper_L.whenPressed(PneumaticsVenturi())
    oi.bumper_R.whenPressed(PneumaticsPiston())

    oi.B.whenPressed(SlapperRaise())
    oi.Y.whenPressed(SlapperSlap())
    oi.A.whenPressed(SlapperHover())
    oi.X.whenPressed(SlapperStop())

    oi.back.whenPressed(SwitchControlMode())
    # oi.start.whenPressed(AutoAlign("tape"))

    oi.B.whenPressed(SetLift(-0.6))
    oi.A.whenPressed(SetLift(0.4))
    oi.start.whenPressed(SetLift(0.3))
    oi.X.whenPressed(FrontSet(0.0))
    oi.Y.whenPressed(FrontSet(0.4))

    logger.info("Commands initialized")
