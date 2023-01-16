from common_files import Telemetry, Protocol
from common_files.constants import Constants
from config import Config
from libs import QMC5883L
from skills.interface import BaseSkill


class CompasSkill(BaseSkill):
    """
       TODO: write smth
    """
    _instance = None
    _sensor = None
    class_name = __qualname__
    skill_tag = Constants.COMPAS_TAG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CompasSkill, cls).__new__(cls)
            cls._sensor = QMC5883L(i2c=Config.i2c_0)
            cls._telemetry = Telemetry()
        return cls._instance

    def run(self) -> None:
        try:
            self._telemetry.coX, self._telemetry.coY, self._telemetry.coZ, _, _ = self._sensor.read()
        except Exception as e:
            self._telemetry.errors = Protocol.SOMETHING_WRONG
