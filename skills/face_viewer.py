from config import Config
from libs import MAX7219
from skills.interface import BaseSkill


class FaceViewer(BaseSkill):
    """
    TODO: write smth
    """

    def __init__(self, bus):
        self.display = MAX7219(bus, Config.ss_pin, 1)

    @property
    def skill_tag(self):
        return "fvs"

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
        self.display.fill(0)
        self.display.show()
        for i in range(8):
            for j in range(8):
                if moods[mood][i][j]:
                    self.display.pixel(7 - i, j, 1)
        self.display.show()
