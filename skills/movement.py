from common_files import Telemetry
from common_files.constants import Constants
from libs import MX1508
from skills.interface import BaseSkill
from common_files.protocol import Protocol


class MovementSkill(BaseSkill):
    """
    TODO: write smth
    """

    _instance = None
    _driver = None

    class_name = __qualname__
    skill_tag = Constants.MOVEMENT_SKILL_TAG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MovementSkill, cls).__new__(cls)
            cls._driver = MX1508()
            cls._telemetry = Telemetry()
        return cls._instance

    def run(self, params: str) -> None:
        split_params = params.split(",")
        try:
            left_wheel_speed = int(split_params[0])
            right_wheel_speed = int(split_params[1])
            self._driver.rotate_wheels(left_speed=left_wheel_speed, right_speed=right_wheel_speed)
            self._telemetry.rwS = right_wheel_speed
            self._telemetry.lwS = left_wheel_speed
        except Exception:
            self._telemetry.errors = Protocol.SOMETHING_WRONG
