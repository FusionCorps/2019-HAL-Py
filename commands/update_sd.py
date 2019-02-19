from wpilib.command import InstantCommand

import dashboard


class UpdateSD(InstantCommand):
    def __init__(self):
        super().__init__("UpdateSD")

    def execute(self):
        dashboard.update()
