from common_files import Telemetry
from common_files.constants import Constants
from config import Config
from libs import LCD_API
from skills.common_funcs import skill_wrapper
from skills.interface import BaseSkill


class LCDDisplaySkill(BaseSkill):
    """
    TODO: write smth
    """
    _instance = None
    _display = None
    class_name = __qualname__
    skill_tag = Constants.LCD_DISPLAY_SKILL_TAG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LCDDisplaySkill, cls).__new__(cls)
            cls._display = LCD_API(Config.i2c_0)
            cls._telemetry = Telemetry()
        return cls._instance

    @skill_wrapper
    def run(self) -> None:
        pass

    def show_text(self, text):
        self._display.putstr(text)
