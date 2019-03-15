import logging
from commands.chassis.chassis_drive import ChassisDrive
from commands.lift.lift_drive import LiftDrive
from commands.lift.lift_drive_grp import LiftDriveGroup
from commands.lift.lift_set import LiftSet
from commands.wait import Wait

from wpilib.command import CommandGroup

import subsystems
from subsystems.lift import Position


class LiftGroup(CommandGroup):
    def __init__(self):
        super().__init__("LiftGroup")
        self.logger = logging.getLogger("LiftGroup")

        # self.addSequential(LiftSet(Position.BOTH_DOWN))
        self.addSequential(LiftDriveGroup(5))

        # self.addSequential(LiftSet(Position.FRONT_UP))

        # self.addSequential(ChassisDrive(0.3, 0.0, 3))
        # self.addParallel(LiftSet(Position.BACK_UP))

    def initialize(self):
        pass

    def isFinished(self):
        return False
