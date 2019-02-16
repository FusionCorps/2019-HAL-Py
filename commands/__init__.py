import logging

import oi

from .intake.eject import IntakeEject
from .intake.halt import IntakeHalt
from .intake.intake import IntakeIntake
from .intake.shoot import IntakeShoot
from .joystick_drive import JoystickDrive
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
    oi.start.whenPressed(PneumaticsClose())

    oi.B.whenPressed(SlapperRaise())
    oi.Y.whenPressed(SlapperSlap())
    oi.A.whenPressed(SlapperHover())
    oi.X.whenPressed(SlapperStop())

    oi.back.whenPressed(SwitchControlMode())

    logger.info("Commands initialized")
