import logging

from ctre import WPI_TalonSRX
from wpilib import ADXRS450_Gyro, BuiltInAccelerometer, Ultrasonic
from wpilib.command import Subsystem

import robotmap
from common.fusion_drive import FusionDrive


class SubChassis(Subsystem):
    """Chassis Subsystem for drivetrain, etc."""

    def __init__(self):
        super().__init__("Chassis")
        self.logger = logging.getLogger("Chassis")

        self._talon_f_l = WPI_TalonSRX(robotmap.talon_f_l)
        self._talon_f_r = WPI_TalonSRX(robotmap.talon_f_r)
        self._talon_b_l = WPI_TalonSRX(robotmap.talon_b_l)
        self._talon_b_r = WPI_TalonSRX(robotmap.talon_b_r)

        self._talons = [self._talon_f_l, self._talon_f_r, self._talon_b_l, self._talon_b_r]

        for talon in self._talons:
            talon.configMotionCruiseVelocity(
                int((robotmap.chassis_max_vel / robotmap.chassis_whl_diameter)
                    * robotmap.chassis_encoder_counts_per_rev), 0)
            talon.configMotionAcceleration(
                int((robotmap.chassis_max_vel / robotmap.chassis_whl_diameter)
                    * robotmap.chassis_encoder_counts_per_rev), 0)

            talon.config_kF(0, robotmap.chassis_fpid[0], 0)
            talon.config_kP(0, robotmap.chassis_fpid[1], 0)
            talon.config_kI(0, robotmap.chassis_fpid[2], 0)
            talon.config_kD(0, robotmap.chassis_fpid[3], 0)
            talon.config_IntegralZone(0, 0, 0)

            talon.configPeakOutputForward(1.0, 0)
            talon.configPeakOutputReverse(-1.0, 0)

            talon.set(0.0)

        # Drive class instance & following
        self.drive = FusionDrive(self._talon_f_l, self._talon_f_r)
        self._talon_b_l.follow(self._talon_f_l)
        self._talon_b_r.follow(self._talon_f_r)

        # Sensors
        self.sonar = Ultrasonic(
            robotmap.ultrasonic_ping,
            robotmap.ultrasonic_echo,
            Ultrasonic.Unit.kMillimeters,
        )

        self.accelerometer_internal = BuiltInAccelerometer(
            BuiltInAccelerometer.Range.k4G
        )
        self.accel_x, self.accel_y, self.accel_z = None, None, None
        self.reset_accelerometer()

        self.gyro = ADXRS450_Gyro(robotmap.gyro)
        self.gyro.calibrate()

        if robotmap.chassis_zero_acceleration_on_start:
            self.gyro.calibrate()

    def get_x(self):
        """Returns relative x position"""
        return self.accel_x - self._get_x()

    def get_y(self):
        """Returns relative y position"""
        return self.accel_y - self._get_y()

    def get_z(self):
        """Returns relative z position"""
        return self.accel_z - self._get_z()

    def _get_x(self):
        """Internal method that returns the accelerometer x position"""
        return self.accelerometer_internal.getX()

    def _get_y(self):
        """Internal method that returns the accelerometer y position"""
        return self.accelerometer_internal.getY()

    def _get_z(self):
        """Internal method that returns the accelerometer z position"""
        return self.accelerometer_internal.getZ()

    def get_left_position(self, target: int = 0) -> int:
        if target == 0:
            return self._talon_f_l.getQuadraturePosition()
        elif target == 1:
            return self._talon_f_l.getPulseWidthPosition()

    def get_right_position(self, target: int = 0) -> int:
        if target == 0:
            return self._talon_f_r.getQuadraturePosition()
        elif target == 1:
            return self._talon_f_r.getPulseWidthPosition()

    def get_distance(self) -> float:
        """Gets Ultrasonic distance in MM"""
        return self.sonar.getRangeMM()

    def get_talon_spds(self):
        """Returns a list of talon speeds"""
        return (talon.get() for talon in self._talons)

    def reset_encoders(self):
        """Sets all talon quadrature encoders to 0"""
        for talon in self._talons:
            talon.setQuadraturePosition(0, 20)
        self.logger.info("Encoders reset")

    def reset_gyro(self):
        """Zeroes the gyro"""
        self.gyro.reset()
        self.logger.info("Gyro reset")

    def reset_accelerometer(self):
        """Zeroes all accelerometer values"""
        self.accel_x = self._get_x()
        self.accel_y = self._get_y()
        self.accel_z = self._get_z()

    def set_ultrasonic(self, state: bool):
        """Sets Ultrasonic state"""
        self.sonar.setEnabled(state)

    def set_left(self, spd_new: float):
        self._talon_f_l.set(-spd_new)

    def set_right(self, spd_new: float):
        self._talon_f_r.set(spd_new)

    def initDefaultCommand(self):
        from commands.chassis.joystick_drive import JoystickDrive

        self.setDefaultCommand(JoystickDrive())
