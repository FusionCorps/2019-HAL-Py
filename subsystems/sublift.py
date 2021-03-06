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
    # Hab 3 climbing
    CLIMB = (robotmap.lift_height, robotmap.lift_height)
    LBACK = (robotmap.lift_height, 0)
    FRONT = (0, robotmap.lift_height)

    # Hab 2 climbing
    CLIMB2 = (robotmap.lift_height_2, robotmap.lift_height_2)
    LBACK2 = (robotmap.lift_height_2, 0)
    FRONT2 = (0, robotmap.lift_height_2)

    FLUSH = (0, 0)


class SubLift(Subsystem):
    """Subsystem used to raise robot to Habs 2 and 3"""

    def __init__(self):
        super().__init__("Lift")
        self.logger = logging.getLogger("Lift")

        self._talon_lift_front = WPI_TalonSRX(robotmap.talon_lift_front)  # Front lift elevator
        self._talon_lift_back = WPI_TalonSRX(robotmap.talon_lift_back)  # Back lift elevator

        self._lift_talons = [self._talon_lift_front, self._talon_lift_back]

        self._talon_lift_drive = WPI_TalonSRX(robotmap.talon_lift_drive)  # Front rack driving motor
        self._talon_lift_drive.configSelectedFeedbackSensor(
            WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0
            )

        # Setting up FPID system for MotionMagic control
        for talon in self._lift_talons:
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
            talon.configMotionAcceleration(robotmap.lift_characteristics[0], 0)
            talon.configMotionCruiseVelocity(robotmap.lift_characteristics[1], 0)
            talon.configPeakOutputForward(0.8, 0)
            talon.configPeakOutputReverse(-0.8, 0)

            talon.set(0.0)

        # Configures FPID gains for front and back
        self._talon_lift_front.config_kF(0, robotmap.lift_front_fpid[0], 0)
        self._talon_lift_front.config_kP(0, robotmap.lift_front_fpid[1], 0)
        self._talon_lift_front.config_kI(0, robotmap.lift_front_fpid[2], 0)
        self._talon_lift_front.config_kD(0, robotmap.lift_front_fpid[3], 0)

        self._talon_lift_back.config_kF(0, robotmap.lift_back_fpid[0], 0)
        self._talon_lift_back.config_kP(0, robotmap.lift_back_fpid[1], 0)
        self._talon_lift_back.config_kI(0, robotmap.lift_back_fpid[2], 0)
        self._talon_lift_back.config_kD(0, robotmap.lift_back_fpid[3], 0)

        self.reset_encoders()

        self._limit_front = DigitalInput(robotmap.lift_front_limit)
        self._limit_back = DigitalInput(robotmap.lift_back_limit)

        self.position_current = Position.FLUSH  # Default position is FLUSH

    def is_both_motion_magic(self) -> bool:
        """Returns whether both lift talons are in MotionMagic Control Mode"""
        return self.is_front_motion_magic() and self.is_back_motion_magic()

    def is_front_motion_magic(self) -> bool:
        """Returns whether front lift talon is in MotionMagic Control Mode"""
        return self.get_front()[1] is ControlMode.MotionMagic

    def is_back_motion_magic(self) -> bool:
        """Returns whether back lift talon is in MotionMagic Control Mode"""
        return self.get_back()[1] is ControlMode.MotionMagic

    def set_front_characteristics(self, chars: (int, int)):
        """Sets the front max cruise velocity and acceleration from a (vel, acc) tuple format"""
        self.logger.info(f"Front characteristics to {str(chars)}")
        self._talon_lift_front.configMotionCruiseVelocity(chars[0])
        self._talon_lift_front.configMotionAcceleration(chars[1])

    def set_back_characteristics(self, chars: (int, int)):
        """Sets the back max cruise velocity and acceleration from a (vel, acc) tuple format"""
        self.logger.info(f"Back  characteristics to {str(chars)}")
        self._talon_lift_back.configMotionCruiseVelocity(chars[0])
        self._talon_lift_back.configMotionAcceleration(chars[1])

    def set_both_characteristics(self, chars: (int, int)):
        """Sets both max cruise velocities and acceleration from a (vel, acc) tuple format"""
        self.set_front_characteristics(chars)
        self.set_back_characteristics(chars)

    def set_back_fpid(self, fpid: (float, float, float, float)):
        """Sets the back lift talon's FPID gains"""
        self.logger.info(f"Back  FPID to {str(fpid)}")
        self._talon_lift_back.config_kF(0, fpid[0], 0)
        self._talon_lift_back.config_kP(0, fpid[1], 0)
        self._talon_lift_back.config_kI(0, fpid[2], 0)
        self._talon_lift_back.config_kD(0, fpid[3], 0)

    def set_front_fpid(self, fpid: (float, float, float, float)):
        """Sets the front lift talon's FPID gains"""
        self.logger.info(f"Front FPID to {str(fpid)}")
        self._talon_lift_front.config_kF(0, fpid[0], 0)
        self._talon_lift_front.config_kP(0, fpid[1], 0)
        self._talon_lift_front.config_kI(0, fpid[2], 0)
        self._talon_lift_front.config_kD(0, fpid[3], 0)

    def set_both_fpid(self, fpid: (float, float, float, float)):
        """Sets both lift talons' FPID gains"""
        self.set_back_fpid(fpid)
        self.set_front_fpid(fpid)

    def set_back(self, target_magnitude, target: int = 0):
        """Sets Back Lift Talon to new MotionMagic position specified in `pos_new`
        Parameters
        ---
        `pos_new`: (int) The new position to be set"""
        if target is 0:
            self._talon_lift_back.set(ControlMode.MotionMagic, -target_magnitude)
        elif target is 1:
            self._talon_lift_back.set(ControlMode.PercentOutput, -target_magnitude)

    def set_front(self, target_magnitude, target: int = 0):
        """Sets Front Lift Talon to new MotionMagic position specified in `pos_new`
        Parameters
        ---
        `pos_new`: (int) The new position to be set"""
        if target is 0:
            self._talon_lift_front.set(ControlMode.MotionMagic, target_magnitude)
        elif target is 1:
            self._talon_lift_front.set(ControlMode.PercentOutput, target_magnitude)

    def stop_back(self):
        """Stops Back Lift Talon"""
        if (self._talon_lift_back.get() is not 0.0
                or self._talon_lift_back.getControlMode() is not ControlMode.PercentOutput):
            self._talon_lift_back.set(ControlMode.PercentOutput, 0.0)

    def stop_front(self):
        """Stops Front Lift Talon"""
        if (self._talon_lift_front.get() is not 0.0
                or self._talon_lift_front.getControlMode() is not ControlMode.PercentOutput):
            self._talon_lift_front.set(ControlMode.PercentOutput, 0.0)

    def set_drive(self, target_magnitude, target: int = 0):
        """Sets Lift Drive Talon to new speed
        Parameters
        ---
        `spd` (int) The new speed to be set"""
        if target is 1:
            self._talon_lift_drive.set(ControlMode.MotionMagic, target_magnitude)
        elif target is 0 and not (target_magnitude is self.get_drive()[0]):
            self._talon_lift_drive.set(mode=ControlMode.PercentOutput, demand0=target_magnitude)
        else:
            pass

    def set_position(self, position_target: Position = None):
        """Sets the position (from the `Position` enum) of the lift"""
        if position_target is not None:
            if position_target is not self.position_current:
                self.logger.warning(f"[ {self.position_current.name} -> {position_target.name} ]")

            self.set_back(position_target.value[0])
            self.set_front(position_target.value[1])

            if self.position_current is not position_target:
                self.position_current = position_target
        else:
            pass

    def get_current_position(self) -> Position:
        """Returns the internal target Lift position"""
        return self.position_current

    def get_front(self) -> (float, ControlMode):
        """Returns the front lift talon's speed and ControlMode"""
        return self._talon_lift_front.get(), self._talon_lift_front.getControlMode()

    def get_back(self) -> (float, ControlMode):
        """Returns the back lift talon's speed and ControlMode"""
        return self._talon_lift_back.get(), self._talon_lift_back.getControlMode()

    def get_drive(self) -> (float, ControlMode):
        """Returns the drive talon's speed and ControlMode"""
        return self._talon_lift_drive.get(), self._talon_lift_drive.getControlMode()

    def get_front_limit(self) -> bool:
        """Returns the front limit switch state"""
        return self._limit_front.get()

    def get_back_limit(self) -> bool:
        """Returns the back limit switch state"""
        return self._limit_back.get()

    def set_front_position(self, pos_new, target=0):
        """Sets either the front quadrature or pulse-width encoder to `pos_new`
        Parameters
        ---
        `pos_new`: (int) Number of ticks
        
        `target`: (int) The target device (default `0` for quad, `1` for pulse)"""
        if target is 0:
            self._talon_lift_front.setQuadraturePosition(pos_new, 0)
        elif target is 1:
            self._talon_lift_front.setPulseWidthPosition(pos_new, 0)

    def set_back_position(self, pos_new, target=0):
        """Sets the back quadrature encoder to `pos_new`
        Parameters
        ---
        `pos_new`: (int) Number of ticks
        
        `target`: (int) The target device (default `0` for quad, `1` for pulse)"""
        if target is 0:
            self._talon_lift_back.setQuadraturePosition(pos_new, 0)
        elif target is 1:
            self._talon_lift_back.setPulseWidthPosition(pos_new, 0)

    def get_front_position(self, target=0) -> int:
        """Returns either the quad or pulse-width position of the front lift
        Parameters
        ---
        `target`: (int) The target device (`0` for quad, `1` for pulse)"""
        if target is 0:
            return self._talon_lift_front.getQuadraturePosition()
        elif target is 1:
            return self._talon_lift_front.getPulseWidthPosition()

    def get_back_position(self, target=0) -> int:
        """Returns either the quad or pulse-width position of the back lift
        Parameters
        ---
        `target`: (int) The target device (`0` for quad, `1` for pulse)"""
        if target is 0:
            return self._talon_lift_back.getQuadraturePosition()
        elif target is 1:
            return self._talon_lift_back.getPulseWidthPosition()
        else:
            pass

    def get_drive_position(self, target=0) -> int:
        if target is 0:
            return self._talon_lift_drive.getQuadraturePosition()
        elif target is 1:
            return self._talon_lift_drive.getPulseWidthPosition()

    def reset_front_encoder(self):
        """Sets the front quadrature encoder to 0"""
        self.logger.info("Zeroing front encoder")
        self._talon_lift_front.setQuadraturePosition(0, 0)

    def reset_back_encoder(self):
        """Sets the back quadrature encoder to 0"""
        self.logger.info("Zeroing back encoder")
        self._talon_lift_back.setQuadraturePosition(0, 0)

    def reset_encoders(self):
        """Sets both the front and back quadrature encoders to 0"""
        self.reset_back_encoder()
        self.reset_front_encoder()
