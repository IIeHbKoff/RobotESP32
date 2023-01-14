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

    def run(self) -> None:
        try:
            self._driver.rotate_wheels(left_speed=int(self._telemetry.lws), right_speed=int(self._telemetry.rws))
        except Exception as e:
            self._telemetry.errors = Protocol.SOMETHING_WRONG
