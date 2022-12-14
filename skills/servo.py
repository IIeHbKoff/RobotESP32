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
            cls._servos = Config.servos_channels
            cls._servo_driver = PCA9685(
                i2c=Config.i2c_0,
                address=Config.servo_board_i2c_addr,
                inverted_channels=(channel["number"] for channel in cls._servos if channel["is_inverted"] is True)
            )
        return cls._instance

    def run(self, params: str) -> str:

        split_params = params.split(",")
        servo = split_params[0]
        servo_value = int(split_params[1])

        if servo is None:
            return str(Protocol.ABSENT_SERVO_VALUE)
        else:
            try:
                self._move(channel=self._servos[servo]["number"], servo_value=servo_value)
                return self._create_answer_packet(status_code=Protocol.SUCCESS)
            except KeyError:
                return self._create_answer_packet(status_code=Protocol.ABSENT_SERVO_CHANNEL)
            except Exception as e:
                return self._create_answer_packet(status_code=Protocol.SOMETHING_WRONG)

    def _move(self, channel, servo_value):
        self._servo_driver.position(index=channel, degrees=servo_value)

    def _create_answer_packet(self, status_code, data=None):
        return f"{self.skill_tag}:{data},{status_code}"
