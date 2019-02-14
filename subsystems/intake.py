from ctre import WPI_TalonSRX
from wpilib.command import PIDSubsystem

import robotmap


class Intake(PIDSubsystem):
    def __init__(self, p, i, d):
        super().__init__(p, i, d, name="Intake")
        self._talon = WPI_TalonSRX(robotmap.talon_intake)

    def returnPIDInput(self):
        return self._talon.getBusVoltage()

    def usePIDOutput(self, output):
        self._talon.pidWrite(output)

    def initDefaultCommand(self):
        # from commands.intake.halt import IntakeHalt

        # self.setDefaultCommand(IntakeHalt())
        pass
