import logging

from wpilib import Notifier
from wpilib.command import InstantCommand

import dashboard


class UpdateClass(object):
    def run(self):
        dashboard.update()


class UpdateSD(InstantCommand):
    def __init__(self):
        super().__init__("UpdateSD")
        self.notifier = Notifier(run=UpdateClass().run())
        self.logger = logging.getLogger("UpdateSD")

    def initialize(self):
        self.logger.info("Starting periodic update")
        self.notifier.startPeriodic(1.0)

    def execute(self):
        pass

    def isFinished(self):
        pass
