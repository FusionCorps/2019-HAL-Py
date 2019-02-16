from wpilib.command import InstantCommand

import robotmap
import subsystems


class SlapperStop(InstantCommand):
    def __init__(self):
        super().__init__("SlapperStop")
        self.requires(subsystems._slapper)

    def initialize(self):
        if subsystems._slapper.slapper.get() == 0.0:
            pass
        else:
            subsystems._slapper.slapper.set(0.0)
