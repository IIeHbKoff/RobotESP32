from common_files import Telemetry
from common_files.constants import Constants
from config import Config
from libs import HCSR04
from skills.common_funcs import skill_wrapper
from skills.interface import BaseSkill


class DistanceMeterSkill(BaseSkill):
    """
    TODO: write smth
    """
    _instance = None
    _sensor = None
    class_name = __qualname__
    skill_tag = Constants.DISTANCE_METER_SKILL_TAG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DistanceMeterSkill, cls).__new__(cls)
            cls._sensor = HCSR04(echo_pin=Config.hc_sr04_echo, trigger_pin=Config.hc_sr04_trigger)
            cls._telemetry = Telemetry()
        return cls._instance

    @skill_wrapper
    def run(self) -> None:
        self._telemetry.dist = self._sensor.distance_mm()
