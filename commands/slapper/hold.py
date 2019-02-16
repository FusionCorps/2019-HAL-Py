from wpilib.command import InstantCommand

import robotmap
import subsystems


class SlapperHold(InstantCommand):
    def __init__(self):
        super().__init__("SlapperHold")
        if robotmap.control_mode == 1:
            self.requires(subsystems._slapper)
        else:
            pass

    def initialize(self):
        if robotmap.control_mode == 1:
            if subsystems._slapper.slapper.get() == robotmap.spd_slapper_hold:
                pass
            else:
                subsystems._slapper.slapper.set(robotmap.spd_slapper_hold)
        else:
            pass
