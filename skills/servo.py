from common_files import Telemetry
from common_files.constants import Constants
from libs.pca9685 import PCA9685
from config import Config
from skills.interface import BaseSkill
from common_files.protocol import Protocol


class ServoSkill(BaseSkill):
    """
    TODO: write smth
    """
    _instance = None
    _servo_driver = None
    _servos = None

    class_name = __qualname__
    skill_tag = Constants.SERVO_SKILL_TAG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServoSkill, cls).__new__(cls)
            cls._servos = Constants.SERVOS_CHANNELS
            cls._servo_driver = PCA9685(
                i2c=Config.i2c_0,
                address=Config.servo_board_i2c_addr,
                inverted_channels=(channel_number for channel_number, channel_data in cls._servos.items()
                                   if channel_data["is_inverted"] is True)
            )
            cls._telemetry = Telemetry()
        return cls._instance

    def run(self, params: str) -> None:
        split_params = params.split(",")
        servo = int(split_params[0])
        servo_value = int(split_params[1])

        if servo is None:
            self._telemetry.errors = Protocol.ABSENT_SERVO_VALUE
        else:
            try:
                self._servo_driver.position(index=servo, degrees=servo_value)
                self._telemetry.__setattr__(f"sch{servo}", servo_value)
            except KeyError:
                self._telemetry.errors = Protocol.ABSENT_SERVO_CHANNEL
            except Exception as e:
                self._telemetry.errors = Protocol.SOMETHING_WRONG
