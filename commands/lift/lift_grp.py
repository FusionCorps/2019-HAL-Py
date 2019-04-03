import logging

from wpilib.command import CommandGroup

from commands.chassis.chassis_drive import ChassisDrive
from commands.lift.lift_drive import LiftDrive
from commands.lift.lift_set import LiftSet
from subsystems.sublift import Position


class LiftGroup(CommandGroup):
    """CommandGroup for climbing Hab 3"""
    def __init__(self):
        super().__init__("LiftGroup")
        self.logger = logging.getLogger("LiftGroup")

        self.addSequential(LiftSet(Position.CLIMB))
        self.addSequential(LiftDrive(0.6, 2))
        self.addSequential(LiftSet(Position.LBACK))
        self.addSequential(ChassisDrive(0.3, 0.0, 1.5))
        self.addSequential(LiftSet(Position.FLUSH))
        self.addSequential(ChassisDrive(0.3, 0.0, 1))

    def initialize(self):
        self.logger.warning("Starting")

    def execute(self):
        pass

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        self.clearRequirements()
        self.logger.warning("Ended")
