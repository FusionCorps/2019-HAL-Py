import logging

from wpilib.command import CommandGroup

from commands.chassis.chassis_drive import ChassisDrive
from commands.chassis.chassis_stop import ChassisStop
from commands.lift.lift_drive import LiftDrive, LiftDrive2
from commands.lift.lift_set import LiftSet
from subsystems.sublift import Position


class ClimbHab3(CommandGroup):
    """CommandGroup for climbing Hab 3"""

    def __init__(self):
        super().__init__("ClimbHab3")
        self.logger = logging.getLogger("ClimbHab3")

        self.addParallel(ChassisStop())
        self.addSequential(LiftSet(Position.CLIMB))
        self.addSequential(LiftDrive(0.6, 2))
        self.addSequential(LiftSet(Position.LBACK))
        self.addSequential(ChassisDrive(0.3, 0.0, 1.4))
        self.addParallel(ChassisStop())
        self.addSequential(LiftSet(Position.FLUSH))
        self.addSequential(ChassisDrive(0.3, 0.0, 0.8))

    def initialize(self):
        self.logger.warning("Starting to climb Hab 3")

    def execute(self):
        pass

    def isFinished(self):
        return not any(entry.command.isRunning() for entry in self.commands)

    def interrupted(self):
        self.end()

    def end(self):
        self.logger.warning("Finished climbing Hab 3")


class ClimbHab2(CommandGroup):
    """CommandGroup for climbing Hab 2"""

    def __init__(self):
        super().__init__("ClimbHab2")
        self.logger = logging.getLogger("ClimbHab2")

        self.addParallel(ChassisStop())
        self.addSequential(LiftSet(Position.CLIMB2))
        self.addSequential(LiftDrive2(0.5, 2))
        self.addSequential(LiftSet(Position.LBACK2))
        self.addSequential(ChassisDrive(0.3, 0.0, 2))
        self.addParallel(ChassisStop())
        self.addSequential(LiftSet(Position.FLUSH))
        self.addSequential(ChassisDrive(0.3, 0.0, 2))

    def initialize(self):
        self.logger.warning("Starting to climb Hab 2")

    def execute(self):
        pass

    def isFinished(self):
        return not any(entry.command.isRunning() for entry in self.commands)

    def interrupted(self):
        self.end()

    def end(self):
        self.logger.warning("Finished climbing Hab 2")
