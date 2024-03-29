from common_files import Telemetry
from common_files.constants import Constants
from config import Config
from libs import MAX7219
from skills.interface import BaseSkill
from common_files.protocol import Protocol


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

    def run(self) -> None:
        data = self._telemetry.mood
        try:
            self._show(data)
        except Exception as e:
            self._telemetry.errors = Protocol.SOMETHING_WRONG

    def _show(self, data: list):
        self._display.fill(0)
        self._display.show()
        for i in range(8):
            for j in range(8):
                if data[i] & (1 << (7 - j)):
                    self._display.pixel(7 - i, j, 1)
        self._display.show()
