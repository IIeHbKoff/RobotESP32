from config import Config
from libs import MAX7219
from skills.interface import BaseSkill


class FaceViewSkill(BaseSkill):
    """
    TODO: write smth
    """
    _instance = None
    _display = None

    class_name = __qualname__
    skill_tag = "fvs"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FaceViewSkill, cls).__new__(cls)
            cls._display = MAX7219(Config.spi_1, Config.ss_pin, 1)
        return cls._instance

    def run(self, params: dict) -> dict:
        mood = params.get("mood")
        if mood is None:
            return {"status": False, "reason": "absent mood"}
        else:
            try:
                self._show_mood(mood)
                return {"status": True, "reason": "ok"}
            except KeyError:
                return {"status": False, "reason": "wrong mood"}

    def _show_mood(self, mood: str):
        moods = {
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
            "connected": [[0, 0, 0, 1, 1, 0, 0, 0],
                          [0, 0, 0, 1, 1, 0, 0, 0],
                          [0, 0, 0, 1, 1, 0, 0, 0],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [0, 0, 0, 1, 1, 0, 0, 0],
                          [0, 0, 0, 1, 1, 0, 0, 0],
                          [0, 0, 0, 1, 1, 0, 0, 0], ],
        }
        self._display.fill(0)
        self._display.show()
        for i in range(8):
            for j in range(8):
                if moods[mood][i][j]:
                    self._display.pixel(7 - i, j, 1)
        self._display.show()
