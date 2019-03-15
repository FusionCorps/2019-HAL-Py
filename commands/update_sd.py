from wpilib import Notifier
from wpilib.command import InstantCommand

import dashboard


class UpdateFunc:
    def run(self):
        print("Updating smartdashboard")
        dashboard.update()


class UpdateSD(InstantCommand):
    def __init__(self):
        super().__init__("UpdateSD")
        self.notifier = Notifier(UpdateFunc().run())

    def initialize(self):
        self.notifier.startPeriodic(0.5)

    def execute(self):
        pass

    def isFinished(self):
        pass
