from ctre import WPI_VictorSPX
from wpilib.command import PIDSubsystem

import robotmap


class Intake(PIDSubsystem):
    def __init__(self, p, i, d):
        super().__init__(p, i, d, name="Intake")
        self._victor = WPI_VictorSPX(robotmap.talon_intake)

    def returnPIDInput(self):
        return self._victor.getBusVoltage()

    def usePIDOutput(self, output):
        self._victor.pidWrite(output)

    def initDefaultCommand(self):
        from commands.intake.halt import IntakeHalt

        self.setDefaultCommand(IntakeHalt())
