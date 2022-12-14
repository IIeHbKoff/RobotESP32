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
        "connecting": [[0, 0, 0, 1, 1, 0, 0, 0],
                       [0, 0, 0, 1, 1, 0, 0, 0],
                       [0, 0, 0, 1, 1, 0, 0, 0],
                       [1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1],
                       [0, 0, 0, 1, 1, 0, 0, 0],
                       [0, 0, 0, 1, 1, 0, 0, 0],
                       [0, 0, 0, 1, 1, 0, 0, 0], ],
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
        return cls._instance

    def run(self, params: str) -> str:
        split_params = params.split(",")
        try:
            mood = split_params[0]
            self._show(self.symbols.get(mood))
            return self._create_answer_packet(status_code=Protocol.SUCCESS)
        except KeyError:
            return self._create_answer_packet(status_code=Protocol.ABSENT_MOOD)
        except Exception as e:
            return self._create_answer_packet(status_code=Protocol.SOMETHING_WRONG)

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

    def _create_answer_packet(self, status_code, data=None):
        return f"{self.skill_tag}:{data},{status_code}"
