from libs import MX1508


class MovementSkill:
    def __init__(self):
        self.driver = MX1508()

    def move_forward(self, speed: int) -> None:
        self.driver.move_forward(speed=speed)

    def move_backward(self, speed: int) -> None:
        self.driver.move_backward(speed=speed)

    def move_left(self, speed: int) -> None:
        self.driver.move_left(speed=speed)

    def move_right(self, speed: int) -> None:
        self.driver.move_right(speed=speed)

    def stop(self) -> None:
        self.driver.stop()
