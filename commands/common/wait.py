import time

from wpilib.command import Command


class Wait(Command):
    def __init__(self, time_wait):
        super().__init__("Wait")
        self.time_wait = time_wait

    def initialize(self):
        time.sleep(self.time_wait)

    def isFinished(self):
        return True

    def interrupted(self):
        pass

    def end(self):
        pass
