import logging

from wpilib.command import Command

import subsystems


class DuckbillSet(Command):
    def __init__(self, state_target, time=0):
        super().__init__(self.__class__.__name__, timeout=time)
        self.requires(subsystems.duckbill)
        self.state_target = state_target
        self.logger = logging.getLogger("DuckbillSet")

    def initialize(self):
        if subsystems.duckbill.get_state() is not self.state_target:
            subsystems.duckbill.set_state(self.state_target)
        else:
            pass

    def isFinished(self):
        return False

    def execute(self):
        pass

    def interrupted(self):
        self.end()

    def end(self):
        pass
