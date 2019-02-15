import logging

import oi

from .pneumatics.close import PneumaticsClose

# from .intake.eject import IntakeEject
# from .intake.halt import IntakeHalt
# from .intake.intake import IntakeIntake
# from .intake.shoot import IntakeShoot
# from .joystick_drive import JoystickDrive
from .pneumatics.piston import PneumaticsPiston
from .pneumatics.venturi import PneumaticsVenturi
from .switch_control_mode import SwitchControlMode


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    oi.X.whenPressed(PneumaticsVenturi())
    oi.X.whenReleased(PneumaticsPiston())
    oi.A.whenPressed(PneumaticsClose())
    oi.bumper_L.whenPressed(SwitchControlMode(0))
    oi.bumper_R.whenPressed(SwitchControlMode(1))

    logger.info("Commands initialized")
