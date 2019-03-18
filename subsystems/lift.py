import logging
from enum import Enum

from ctre import ControlMode, WPI_TalonSRX
from ctre.basemotorcontroller import DemandType
from wpilib import DigitalInput
from wpilib.command import Subsystem

import robotmap


class Position(Enum):
    """
    Sets MotionMagic position based on (back, front) value
    """

    BOTH_DOWN = (robotmap.lift_height, robotmap.lift_height)
    BOTH_UP = (0, 0)
    BACK_DOWN = (robotmap.lift_height, 0)
    FRONT_DOWN = (0, robotmap.lift_height)


class Lift(Subsystem):
    def __init__(self):
        super().__init__("Lift")
        self.logger = logging.getLogger("Lift")

        self.talon_drive_CFront = WPI_TalonSRX(robotmap.talon_lift_front)
        self.talon_drive_CBack = WPI_TalonSRX(robotmap.talon_lift_back)

        self.lift_talons = [self.talon_drive_CFront, self.talon_drive_CBack]

        self.talon_drive_CDRive = WPI_TalonSRX(robotmap.talon_lift_drive)

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
            talon.configPeakOutputForward(0.8, 0)
            talon.configPeakOutputReverse(-0.8, 0)

            talon.set(0.0)

        self.frontFPID = [0.025, 0.8, 0.05, 0]
        self.backFPID = [0.025, 0.8, 0.05, 0]

        self.talon_drive_CFront.config_kF(0, self.frontFPID[0], 0)
        self.talon_drive_CFront.config_kP(0, self.frontFPID[1], 0)
        self.talon_drive_CFront.config_kI(0, self.frontFPID[2], 0)
        self.talon_drive_CFront.config_kD(0, self.frontFPID[3], 0)

        self.talon_drive_CBack.config_kF(0, self.backFPID[0], 0)
        self.talon_drive_CBack.config_kP(0, self.backFPID[1], 0)
        self.talon_drive_CBack.config_kI(0, self.backFPID[2], 0)
        self.talon_drive_CBack.config_kD(0, self.backFPID[3], 0)

        self.reset_encoders()

        self.CFront_limit = DigitalInput(robotmap.lift_front_limit)
        self.CBack_limit = DigitalInput(robotmap.lift_back_limit)

        self.position_current = Position.BOTH_UP

    def set_back(self, pos_new):
        """Sets Back Lift Talon to new MotionMagic position specified in `pos_new`
        Parameters
        ---
        `pos_new`: (int) The new position to be set"""
        self.talon_drive_CBack.set(ControlMode.MotionMagic, pos_new)

    def set_front(self, pos_new):
        """Sets Front Lift Talon to new MotionMagic position specified in `pos_new`
        Parameters
        ---
        `pos_new`: (int) The new position to be set"""
        self.talon_drive_CFront.set(ControlMode.MotionMagic, pos_new)

    def stop_back(self):
        """Stops Back Lift Talon"""
        self.talon_drive_CBack.set(ControlMode.PercentOutput, 0.0)

    def stop_front(self):
        """Stops Front Lift Talon"""
        self.talon_drive_CFront.set(ControlMode.PercentOutput, 0.0)

    def set_drive(self, spd):
        """Sets Lift Drive Talon to new speed
        Parameters
        ---
        `spd` (int) The new speed to be set"""
        self.talon_drive_CDRive.set(spd)

    def set_position(self, position_target=None):
        """Sets the position (from the `Position` enum) of the lift"""
        if position_target is not None:
            if position_target is not self.position_current:
                self.logger.warning(
                    "Position Target | ["
                    + self.position_current.name
                    + " -> "
                    + position_target.name
                    + "]"
                )
                for talon in self.lift_talons:
                    talon.setIntegralAccumulator(0, 0, 0)

            self.set_back(position_target.value[0])
            self.set_front(position_target.value[1])

            if self.position_current is not position_target:
                self.position_current = position_target
        else:
            pass

    def get_current_position(self):
        """Returns the internal target Lift position"""
        return self.position_current

    def get_front_limit(self):
        return self.CFront_limit.get()

    def get_back_limit(self):
        return self.CBack_limit.get()

    def set_front_position(self, pos_new, target=0):
        """Sets either the front quadrature or pulse-width encoder to `pos_new`
        Parameters
        ---
        `pos_new`: (int) Number of ticks
        
        `target`: (int) The target device (default `0` for quad, `1` for pulse)"""
        if target is 0:
            self.talon_drive_CFront.setQuadraturePosition(pos_new, 0)
        elif target is 1:
            self.talon_drive_CFront.setPulseWidthPosition(pos_new, 0)

    def set_back_position(self, pos_new, target=0):
        """Sets the back quadrature encoder to `pos_new`
        Parameters
        ---
        `pos_new`: (int) Number of ticks
        
        `target`: (int) The target device (default `0` for quad, `1` for pulse)"""
        if target is 0:
            self.talon_drive_CBack.setQuadraturePosition(pos_new, 0)
        elif target is 1:
            self.talon_drive_CBack.setPulseWidthPosition(pos_new, 0)

    def get_front_position(self, target=0):
        """Returns either the quad or pulse-width position of the front lift
        Parameters
        ---
        `target`: (int) The target device (`0` for quad, `1` for pulse)"""
        if target is 0:
            return self.talon_drive_CFront.getQuadraturePosition()
        elif target is 1:
            return self.talon_drive_CFront.getPulseWidthPosition()

    def get_back_position(self, target=0):
        """Returns either the quad or pulse-width position of the back lift
        Parameters
        ---
        `target`: (int) The target device (`0` for quad, `1` for pulse)"""
        if target is 0:
            return self.talon_drive_CBack.getQuadraturePosition()
        elif target is 1:
            return self.talon_drive_CBack.getPulseWidthPosition()
        else:
            pass

    def reset_front_encoder(self):
        """Sets the front quadrature encoder to 0"""
        self.logger.info("Zeroing front encoder")
        self.talon_drive_CFront.setQuadraturePosition(0, 0)

    def reset_back_encoder(self):
        """Sets the back quadrature encoder to 0"""
        self.logger.info("Zeroing back encoder")
        self.talon_drive_CBack.setQuadraturePosition(0, 0)

    def reset_encoders(self):
        """Sets both the front and back quadrature encoders to 0"""
        self.reset_back_encoder()
        self.reset_front_encoder()
