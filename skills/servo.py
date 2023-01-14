from common_files import Telemetry
from common_files.constants import Constants
from libs.pca9685 import Servos
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
            cls._servo_driver = Servos(
                i2c=Config.i2c_0,
                address=Config.servo_board_i2c_addr
            )
            cls._telemetry = Telemetry()
        return cls._instance

    def run(self) -> None:
        for number, info in Constants.SERVOS_CHANNELS.items():
            try:
                self._servo_driver.position(index=number, degrees=int(getattr(self._telemetry, info["name"])))
            except Exception as e:
                self._telemetry.errors = Protocol.SOMETHING_WRONG
