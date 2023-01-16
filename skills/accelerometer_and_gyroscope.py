from common_files import Telemetry
from common_files.constants import Constants
from config import Config
from libs import MPU6050
from skills.common_funcs import skill_wrapper
from skills.interface import BaseSkill


class AccelerometerAndGyroscopeSkill(BaseSkill):
    """
       TODO: write smth
    """
    _instance = None
    _sensor = None
    class_name = __qualname__
    skill_tag = Constants.ACCELEROMETER_AND_GYROSCOPE_TAG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AccelerometerAndGyroscopeSkill, cls).__new__(cls)
            cls._sensor = MPU6050(i2c=Config.i2c_0)
            cls._telemetry = Telemetry()
        return cls._instance

    @skill_wrapper
    def run(self) -> None:
        data = self._sensor.get_values()
        self._telemetry.acX = data["AcX"]
        self._telemetry.acY = data["AcY"]
        self._telemetry.acZ = data["AcZ"]
        self._telemetry.gyX = data["GyX"]
        self._telemetry.gyY = data["GyY"]
        self._telemetry.gyZ = data["GyZ"]
