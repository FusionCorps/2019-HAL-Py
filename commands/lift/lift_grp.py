import logging

from wpilib.command import CommandGroup

from commands.chassis.chassis_drive import ChassisDrive
from commands.lift.lift_drive import LiftDrive
from commands.lift.lift_set import LiftSet
from subsystems.sublift import Position


class LiftGroup(CommandGroup):
    def __init__(self):
        super().__init__("LiftGroup")
        self.logger = logging.getLogger("LiftGroup")

        self.addSequential(LiftSet(Position.BOTH_DOWN))
        self.addSequential(LiftDrive(0.6, 3))
        self.addSequential(ChassisDrive(0.5, 0.0, 2))
        self.addSequential(LiftSet(Position.FRONT_UP))
        self.addParallel(ChassisDrive(0.5, 0.0, 3))
        self.addSequential(LiftSet(Position.BACK_UP))

    def initialize(self):
        pass

    def execute(self):
        pass

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        self.clearRequirements()
