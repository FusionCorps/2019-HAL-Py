import logging

from wpilib.command import Command

import subsystems
from subsystems.subduckbill import StateDuckbill


class DuckbillSwitch(Command):
    def __init__(self, time=0):
        super().__init__(self.__class__.__name__, timeout=time)
        self.requires(subsystems.duckbill)
        self.logger = logging.getLogger("DuckbillSet")

    def initialize(self):
        if subsystems.duckbill.get_state() is StateDuckbill.DOWN:
            subsystems.duckbill.set_state(StateDuckbill.UP)
        elif subsystems.duckbill.get_state() is StateDuckbill.UP:
            subsystems.duckbill.set_state(StateDuckbill.DOWN)
        else:
            subsystems.duckbill.set_state(StateDuckbill.HALT)

    def isFinished(self):
        return True

    def execute(self):
        pass

    def interrupted(self):
        self.end()

    def end(self):
        pass
