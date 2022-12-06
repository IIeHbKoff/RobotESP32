from libs import MX1508
from skills.interface import BaseSkill


class MovementSkill(BaseSkill):
    """
    TODO: write smth
    """
    def __init__(self, bus):
        self._driver = MX1508()

    @property
    def skill_tag(self):
        return "mws"

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
