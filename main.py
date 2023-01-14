import time

import skills
from common_files import Constants, Protocol, Telemetry
from common_files.utils import Utils
from networking import NetworkConnection


class Robot:
    def __init__(self) -> None:
        self.networking = NetworkConnection()
        self.protocol = Protocol()
        self.utils = Utils()
        # self.viewer = skills.FaceViewSkill()
        self.telemetry = Telemetry()
        self.frame_time = 1000/Constants.WINDOW_FPS

    def run(self) -> None:
        self._connecting()
        self._life_cycle()
        self._i_will_be_back()

    def _connecting(self) -> None:
        # self._show_technical_info("connecting")
        self.networking.connect_to_wifi()
        time.sleep(3)
        self.utils.connect()
        # self._show_technical_info("connected")

    def _life_cycle(self) -> None:
        while True:
            self.utils.get_and_fill_cmds()
            for name, skill in skills.skill_dict.items():
                skill().run()
            self.utils.send_telemetry()
            del self.telemetry.errors

    def _i_will_be_back(self) -> None:
        self.utils.disconnect()
        self.networking.disconnect()


if __name__ == "__main__":
    robot = Robot()
    robot.run()
