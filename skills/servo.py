from libs.pca9685 import PCA9685
from config import Config
from skills.interface import BaseSkill


class ServosSkill(BaseSkill):
    """
    TODO: write smth
    """
    def __init__(self, bus):
        self._servo_driver = PCA9685(i2c=bus, address=Config.servo_board_i2c_addr, inverted_channels=(2,))
        self._servos = {"head": 0, "right_arm": 1, "left_arm": 2}

    @property
    def skill_tag(self):
        return "sds"

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
