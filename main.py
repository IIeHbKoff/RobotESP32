from skills import MovementSkill


class Robot:
    def __init__(self):
        self.mv_skill = MovementSkill()

    def run(self):
        while True:
            pass


if __name__ == "__main__":
    robot = Robot()
    robot.run()
