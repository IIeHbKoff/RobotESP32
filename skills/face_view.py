from common_files import Telemetry
from common_files.constants import Constants
from config import Config
from libs import MAX7219
from skills.common_funcs import skill_wrapper
from skills.interface import BaseSkill


class FaceViewSkill(BaseSkill):
    """
    TODO: write smth
    """
    _instance = None
    _display = None
    class_name = __qualname__
    skill_tag = Constants.FACE_VIEWER_SKILL_TAG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FaceViewSkill, cls).__new__(cls)
            cls._display = MAX7219(Config.spi_1, Config.ss_pin, 1)
            cls._telemetry = Telemetry()
        return cls._instance

    @skill_wrapper
    def run(self) -> None:
        self._show(self._telemetry.mood)

    def _show(self, data: list):
        self._display.fill(0)
        self._display.show()
        for i in range(8):
            for j in range(8):
                if data[i] & (1 << (7 - j)):
                    self._display.pixel(7 - i, j, 1)
        self._display.show()
