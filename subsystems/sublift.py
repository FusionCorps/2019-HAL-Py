import logging
from enum import Enum

from ctre import ControlMode, WPI_TalonSRX
from wpilib import DigitalInput
from wpilib.command import Subsystem

import robotmap


class Position(Enum):
    """
    Sets MotionMagic position based on (back, front) value
    """

    CLIMB = (robotmap.lift_height, robotmap.lift_height)
    FLUSH = (0, 0)
    LBACK = (robotmap.lift_height, 0)
    LFRONT = (0, robotmap.lift_height)


class SubLift(Subsystem):
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

            talon.selectProfileSlot(0, 0)
            talon.configMotionAcceleration(robotmap.lift_acceleration, 0)
            talon.configMotionCruiseVelocity(robotmap.lift_cruise_velocity, 0)
            talon.configPeakOutputForward(0.8, 0)
            talon.configPeakOutputReverse(-0.8, 0)

            talon.set(0.0)

        self.talon_drive_CFront.config_kF(0, robotmap.lift_front_fpid[0], 0)
        self.talon_drive_CFront.config_kP(0, robotmap.lift_front_fpid[1], 0)
        self.talon_drive_CFront.config_kI(0, robotmap.lift_front_fpid[2], 0)
        self.talon_drive_CFront.config_kD(0, robotmap.lift_front_fpid[3], 0)

        self.talon_drive_CBack.setSensorPhase(True)
        self.talon_drive_CBack.setInverted(True)
        self.talon_drive_CBack.config_kF(0, robotmap.lift_back_fpid[0], 0)
        self.talon_drive_CBack.config_kP(0, robotmap.lift_back_fpid[1], 0)
        self.talon_drive_CBack.config_kI(0, robotmap.lift_back_fpid[2], 0)
        self.talon_drive_CBack.config_kD(0, robotmap.lift_back_fpid[3], 0)

        self.reset_encoders()

        self.CFront_limit = DigitalInput(robotmap.lift_front_limit)
        self.CBack_limit = DigitalInput(robotmap.lift_back_limit)

        self.position_current = Position.FLUSH

    def is_motion_magic_active(self):
        return (self.get_back()[1] is ControlMode.MotionMagic) and (self.get_front()[1] is ControlMode.MotionMagic)

    def set_back_fpid(self, fpid):
        self.talon_drive_CBack.config_kF(0, fpid[0], 0)
        self.talon_drive_CBack.config_kP(0, fpid[1], 0)
        self.talon_drive_CBack.config_kI(0, fpid[2], 0)
        self.talon_drive_CBack.config_kD(0, fpid[3], 0)

    def set_front_fpid(self, fpid):
        self.talon_drive_CFront.config_kF(0, fpid[0], 0)
        self.talon_drive_CFront.config_kP(0, fpid[1], 0)
        self.talon_drive_CFront.config_kI(0, fpid[2], 0)
        self.talon_drive_CFront.config_kD(0, fpid[3], 0)

    def set_back(self, target_magnitude, target=0):
        """Sets Back Lift Talon to new MotionMagic position specified in `pos_new`
        Parameters
        ---
        `pos_new`: (int) The new position to be set"""
        if target is 0:
            self.talon_drive_CBack.set(ControlMode.MotionMagic, -target_magnitude)
        elif target is 1:
            self.talon_drive_CBack.set(ControlMode.PercentOutput, -target_magnitude)

    def set_front(self, target_magnitude, target=0):
        """Sets Front Lift Talon to new MotionMagic position specified in `pos_new`
        Parameters
        ---
        `pos_new`: (int) The new position to be set"""
        if target is 0:
            self.talon_drive_CFront.set(ControlMode.MotionMagic, target_magnitude)
        elif target is 1:
            self.talon_drive_CFront.set(ControlMode.PercentOutput, target_magnitude)

    def stop_back(self):
        """Stops Back Lift Talon"""
        if (
                self.talon_drive_CBack.get() is not 0.0
                or self.talon_drive_CBack.getControlMode() is not ControlMode.PercentOutput
        ):
            self.talon_drive_CBack.set(ControlMode.PercentOutput, 0.0)

    def stop_front(self):
        """Stops Front Lift Talon"""
        if (
                self.talon_drive_CFront.get() is not 0.0
                or self.talon_drive_CFront.getControlMode() is not ControlMode.PercentOutput
        ):
            self.talon_drive_CFront.set(ControlMode.PercentOutput, 0.0)

    def set_drive(self, target_magnitude, target=0):
        """Sets Lift Drive Talon to new speed
        Parameters
        ---
        `spd` (int) The new speed to be set"""
        if target is 1:
            self.talon_drive_CDRive.set(ControlMode.MotionMagic, target_magnitude)
        elif target is 0 and not (target_magnitude is self.get_drive()[0]):
            self.talon_drive_CDRive.set(mode=ControlMode.PercentOutput, demand0=target_magnitude)
        else:
            pass

    def set_position(self, position_target=None):
        """Sets the position (from the `Position` enum) of the lift"""
        if position_target is not None:
            if position_target is not self.position_current:
                self.logger.warning(
                    "[ "
                    + self.position_current.name
                    + " -> "
                    + position_target.name
                    + " ]"
                )

            self.set_back(position_target.value[0])
            self.set_front(position_target.value[1])

            if self.position_current is not position_target:
                self.position_current = position_target
        else:
            pass

    def get_current_position(self):
        """Returns the internal target Lift position"""
        return self.position_current

    def get_front(self):
        return self.talon_drive_CFront.get(), self.talon_drive_CFront.getControlMode()

    def get_back(self):
        return self.talon_drive_CBack.get(), self.talon_drive_CBack.getControlMode()

    def get_drive(self):
        return self.talon_drive_CDRive.get(), self.talon_drive_CDRive.getControlMode()

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

    def get_drive_position(self, target=0):
        if target is 0:
            return self.talon_drive_CDRive.getQuadraturePosition()
        elif target is 1:
            return self.talon_drive_CDRive.getPulseWidthPosition()

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
