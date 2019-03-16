import logging
from enum import Enum

from ctre import ControlMode, WPI_TalonSRX
from ctre.basemotorcontroller import DemandType
from wpilib import DigitalInput
from wpilib.command import Subsystem

import robotmap


class Position(Enum):
    """
    Sets position speeds based on (back, front) value
    """

    BOTH_DOWN = (50000, 50000)
    BOTH_UP = (0, 0)
    BACK_DOWN = (50000, 0)
    FRONT_DOWN = (0, 50000)


class Lift(Subsystem):
    def __init__(self):
        super().__init__("Lift")
        self.logger = logging.getLogger("Lift")

        self.talon_drive_CFront = WPI_TalonSRX(robotmap.talon_lift_CFront)
        self.talon_drive_CBack = WPI_TalonSRX(robotmap.talon_lift_CBack)
        self.lift_talons = [self.talon_drive_CFront, self.talon_drive_CBack]
        self.talon_drive_CDRive = WPI_TalonSRX(robotmap.talon_lift_CDrive)

        self.talon_drive_CDRive.configSelectedFeedbackSensor(
            WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0
        )

        for talon in self.lift_talons:
            talon.configSelectedFeedbackSensor(
                WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0
            )
            talon.configSelectedFeedbackCoefficient(0.5, 0, 0)
            talon.setStatusFramePeriod(
                WPI_TalonSRX.StatusFrameEnhanced.Status_12_Feedback1, 20, 0
            )
            talon.setStatusFramePeriod(
                WPI_TalonSRX.StatusFrameEnhanced.Status_13_Base_PIDF0, 20, 0
            )
            talon.setStatusFramePeriod(
                WPI_TalonSRX.StatusFrameEnhanced.Status_10_MotionMagic, 20, 0
            )
            # talon.setStatusFramePeriod(
            #     WPI_TalonSRX.StatusFrameEnhanced.Status_10_Targets, 20, 0
            # )
            # talon.setStatusFramePeriod(
            #     WPI_TalonSRX.StatusFrameEnhanced.Status_2_Feedback0, 20, 0
            # )

            talon.selectProfileSlot(0, 0)
            talon.configMotionAcceleration(200, 0)
            talon.configMotionCruiseVelocity(24000, 0)
            talon.configPeakOutputForward(1.0, 0)
            talon.configPeakOutputReverse(-1.0, 0)

            talon.set(0.0)

        self.frontFPID = [0.025, 0.8, 0.005, 0.4]
        self.backFPID = [0.025, 0.8, 0.005, 0.4]

        self.talon_drive_CFront.config_kF(0, self.frontFPID[0], 0)
        self.talon_drive_CFront.config_kP(0, self.frontFPID[1], 0)
        self.talon_drive_CFront.config_kI(0, self.frontFPID[2], 0)
        self.talon_drive_CFront.config_kD(0, self.frontFPID[3], 0)

        self.talon_drive_CBack.config_kF(0, self.backFPID[0], 0)
        self.talon_drive_CBack.config_kP(0, self.backFPID[1], 0)
        self.talon_drive_CBack.config_kI(0, self.backFPID[2], 0)
        self.talon_drive_CBack.config_kD(0, self.backFPID[3], 0)

        self.resetEncoders()

        self.CFront_limit = DigitalInput(robotmap.lift_cfront_limit_top)
        self.CBack_limit = DigitalInput(robotmap.lift_cback_limit_top)

        self.position_current = Position.BOTH_UP

    def setBack(self, pos_new):
        """
        Sets Back Lift Talon to new position specified in `pos_new`
        Parameters
        ---
        `pos_new` (int) The new position to be set
        """
        self.talon_drive_CBack.set(ControlMode.MotionMagic, pos_new)

    def setFront(self, pos_new):
        """
        Sets Front Lift Talon to new position specified in `pos_new`
        Parameters
        ---
        `pos_new` (int) The new position to be set
        """
        self.talon_drive_CFront.set(ControlMode.MotionMagic, pos_new)

    def stopBack(self):
        """
        Stops Back Lift Talon
        """
        self.talon_drive_CBack.set(ControlMode.PercentOutput, 0.0)

    def stopFront(self):
        """
        Stops Front Lift Talon
        """
        self.talon_drive_CFront.set(ControlMode.PercentOutput, 0.0)

    def setDrive(self, spd):
        """
        Sets Lift Drive Talon to new speed
        Parameters
        ---
        `spd` (int) The new speed to be set
        """
        self.talon_drive_CDRive.set(spd)

    def setPosition(self, position_target):
        if position_target is not None:
            if position_target is not self.position_current:
                self.logger.warning(
                    "(Position) "
                    + self.position_current.name
                    + " -> "
                    + position_target.name
                )
                for talon in self.lift_talons:
                    talon.setIntegralAccumulator(0, 0, 0)

            self.setBack(position_target.value[0])
            self.setFront(position_target.value[1])
            self.position_current = position_target
        else:
            pass

    def getCurrentPosition(self):
        return self.position_current

    def getFrontLimit(self):
        return self.CFront_limit.get()

    def getBackLimit(self):
        return self.CBack_limit.get()

    def setFrontPosition(self, pos_new):
        self.talon_drive_CFront.setQuadraturePosition(pos_new, 0)

    def setBackPosition(self, pos_new):
        self.talon_drive_CBack.setQuadraturePosition(pos_new, 0)

    def getFrontPosition(self, target=0):
        if target is 0:
            return self.talon_drive_CFront.getQuadraturePosition()
        elif target is 1:
            return self.talon_drive_CFront.getPulseWidthPosition()
        else:
            pass

    def getBackPosition(self, target=0):
        if target is 0:
            return self.talon_drive_CBack.getQuadraturePosition()
        elif target is 1:
            return self.talon_drive_CBack.getPulseWidthPosition()
        else:
            pass

    def resetFrontEncoder(self):
        self.logger.info("Zeroing front encoder")
        self.talon_drive_CFront.setQuadraturePosition(0, 0)

    def resetBackEncoder(self):
        self.logger.info("Zeroing back encoder")
        self.talon_drive_CBack.setQuadraturePosition(0, 0)

    def resetEncoders(self):
        self.resetBackEncoder()
        self.resetFrontEncoder()
