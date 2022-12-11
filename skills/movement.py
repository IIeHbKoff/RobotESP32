from libs import MX1508
from skills.interface import BaseSkill


class MovementSkill(BaseSkill):
    """
    TODO: write smth
    """
    _instance = None
    _driver = None

    class_name = __qualname__
    skill_tag = "mws"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MovementSkill, cls).__new__(cls)
            cls._driver = MX1508()
        return cls._instance

    def run(self, params: dict) -> dict:
        pass

    def _move_forward(self, speed: int) -> None:
        self._driver.move_forward(speed=speed)

    def _move_backward(self, speed: int) -> None:
        self._driver.move_backward(speed=speed)

    def _move_left(self, speed: int) -> None:
        self._driver.move_left(speed=speed)

    def _move_right(self, speed: int) -> None:
        self._driver.move_right(speed=speed)

    def _stop(self) -> None:
        self._driver.stop()
