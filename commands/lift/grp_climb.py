from wpilib.command import CommandGroup

import subsystems


class GrpClimb(CommandGroup):
    def __init__(self):
        super().__init__("GrpClimb")

    def initialize(self):
        from commands.lift.backset import BackSet
        from commands.lift.frontset import FrontSet
        from commands.lift.lraise import SetLift
        from commands.lift.drive import LiftDrive

        self.back_set = BackSet(0.4)
        self.front_set = FrontSet(0.4)
        self.raise_lift = SetLift(-0.6)
        self.drive_lift = LiftDrive(0.4)

        self.addSequential(self.raise_lift)
        self.addSequential(self.front_set)
        self.addSequential(self.drive_lift)
