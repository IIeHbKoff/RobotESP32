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
    symbols = {
        "smile": [[1, 1, 1, 0, 0, 1, 1, 1],
                  [1, 0, 1, 0, 0, 1, 0, 1],
                  [1, 1, 1, 0, 0, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0, 1, 0],
                  [0, 0, 1, 1, 1, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0], ],
        "neutral": [[1, 1, 1, 0, 0, 1, 1, 1],
                    [1, 0, 1, 0, 0, 1, 0, 1],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], ],
        "sad": [[1, 1, 1, 0, 0, 1, 1, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0], ],
        "winking_left_eye": [[0, 0, 0, 0, 0, 1, 1, 1],
                             [1, 1, 1, 0, 0, 1, 0, 1],
                             [0, 0, 0, 0, 0, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 1, 0],
                             [0, 0, 1, 1, 1, 1, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0], ],
        "winking_right_eye": [[1, 1, 1, 0, 0, 0, 0, 0],
                              [1, 0, 1, 0, 0, 1, 1, 1],
                              [1, 1, 1, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 1, 0, 0, 0, 0, 1, 0],
                              [0, 0, 1, 1, 1, 1, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0], ],
        "connecting": [[0, 0, 1, 1, 1, 1, 0, 0],
                       [0, 1, 1, 1, 1, 1, 1, 0],
                       [1, 1, 0, 0, 0, 0, 1, 1],
                       [1, 1, 0, 0, 0, 0, 0, 0],
                       [1, 1, 0, 0, 0, 0, 0, 0],
                       [1, 1, 0, 0, 0, 0, 1, 1],
                       [0, 1, 1, 1, 1, 1, 1, 0],
                       [0, 0, 1, 1, 1, 1, 0, 0], ],
        "connected": [[0, 0, 1, 1, 1, 1, 0, 0],
                      [0, 1, 1, 1, 1, 1, 1, 0],
                      [1, 1, 0, 0, 0, 0, 1, 1],
                      [1, 1, 0, 1, 1, 0, 0, 0],
                      [1, 1, 0, 1, 1, 0, 0, 0],
                      [1, 1, 0, 0, 0, 0, 1, 1],
                      [0, 1, 1, 1, 1, 1, 1, 0],
                      [0, 0, 1, 1, 1, 1, 0, 0], ],
        "void": [[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0], ],
    }
    class_name = __qualname__
    skill_tag = Constants.FACE_VIEWER_SKILL_TAG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FaceViewSkill, cls).__new__(cls)
            cls._display = MAX7219(Config.spi_1, Config.ss_pin, 1)
            cls._telemetry = Telemetry()
        return cls._instance

    def run(self, params: str) -> None:
        split_params = params.split(",")
        try:
            mood = split_params[0]
            self._show(self.symbols.get(mood))
            self._telemetry.mood = mood
        except KeyError:
            self._telemetry.errors = Protocol.ABSENT_MOOD
        except Exception as e:
            self._telemetry.errors = Protocol.SOMETHING_WRONG

    def _show(self, matrix: list):
        self._display.fill(0)
        self._display.show()
        for i in range(8):
            for j in range(8):
                if matrix[i][j]:
                    self._display.pixel(7 - i, j, 1)
        self._display.show()

    def show_tech_info(self, info):
        self._show(self.symbols.get(info))
