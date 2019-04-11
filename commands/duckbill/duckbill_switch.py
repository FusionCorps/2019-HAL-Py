import logging

from wpilib.command import InstantCommand

import subsystems
from subsystems.subduckbill import StateDuckbill


class DuckbillSwitch(InstantCommand):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.requires(subsystems.duckbill)
        self.logger = logging.getLogger("DuckbillSet")

    def initialize(self):
        if subsystems.duckbill.get_state() is StateDuckbill.DOWN:
            subsystems.duckbill.set_state(StateDuckbill.UP)
        elif subsystems.duckbill.get_state() is StateDuckbill.UP:
            subsystems.duckbill.set_state(StateDuckbill.DOWN)
        elif subsystems.duckbill.get_state() is StateDuckbill.HALT:
            subsystems.duckbill.set_state(StateDuckbill.DOWN)
        else:
            raise ValueError
