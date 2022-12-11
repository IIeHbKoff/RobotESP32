from libs.pca9685 import PCA9685
from config import Config
from skills.interface import BaseSkill


class ServoSkill(BaseSkill):
    """
    TODO: write smth
    """
    _instance = None
    _servo_driver = None
    _servos = None

    class_name = __qualname__
    skill_tag = "sds"

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

    def run(self, params: dict) -> dict:
        servo = params.get("servo")
        servo_value = params.get("servo_value")
        if servo is None:
            return {"status": False, "reason": "absent servo param"}
        else:
            try:
                self._move(channel=self._servos[servo], servo_value=servo_value)
            except KeyError:
                return {"status": False, "reason": "absent servo channel"}
            except Exception as e:
                return {"status": False, "reason": e}

    def _move(self, channel, servo_value):
        self._servo_driver.position(index=channel, degrees=servo_value)
