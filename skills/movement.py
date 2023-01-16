from common_files import Telemetry
from common_files.constants import Constants
from libs import MX1508
from skills.common_funcs import skill_wrapper
from skills.interface import BaseSkill


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

    @skill_wrapper
    def run(self) -> None:
        self._driver.rotate_wheels(left_speed=int(self._telemetry.lws), right_speed=int(self._telemetry.rws))
