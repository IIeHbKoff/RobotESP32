from common_files import Telemetry
from common_files.constants import Constants
from config import Config
from libs import BMP280
from skills.common_funcs import skill_wrapper
from skills.interface import BaseSkill


class MicroClimateSkill(BaseSkill):
    """
       TODO: write smth
    """
    _instance = None
    _sensor = None
    class_name = __qualname__
    skill_tag = Constants.MICRO_CLIMATE_SKILL_TAG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MicroClimateSkill, cls).__new__(cls)
            cls._sensor = BMP280(i2c=Config.i2c_0)
            cls._telemetry = Telemetry()
        return cls._instance

    @skill_wrapper
    def run(self) -> None:
        self._telemetry.temperature = self._sensor.temperature()
        self._telemetry.pressure, = self._sensor.pressure()
