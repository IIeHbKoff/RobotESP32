import time

import skills
from common_files import Constants, Protocol, Telemetry
from libs import Redis
from networking import NetworkConnection


class Robot:
    def __init__(self) -> None:
        self.networking = NetworkConnection()
        self.protocol = Protocol()
        self.viewer = skills.FaceViewSkill()
        self.telemetry = Telemetry()
        self.broker = Redis(host=Constants.REDIS_HOST, port=Constants.REDIS_PORT, timeout=Constants.REDIS_TIMEOUT)
        self.frame_time = 1000/Constants.WINDOW_FPS

    def run(self) -> None:
        self._connecting()
        self._life_cycle()
        self._i_will_be_back()

    def _connecting(self) -> None:
        self._show_technical_info("connecting")
        self.networking.connect_to_wifi()
        self.broker.connect()
        self._show_technical_info("connected")

    def _life_cycle(self) -> None:
        while True:
            t1 = time.ticks_ms()
            skill_list = self._get_commands()
            for skill, params in skill_list:
                skills.skill_dict[skill]().run(params)
            self._send_telemetry()
            self._show_technical_info()
            del self.telemetry.errors
            t2 = time.ticks_ms()
            if time.ticks_diff(t2, t1) > self.frame_time:
                print("Slowly")
            else:
                time.sleep(self.frame_time-time.ticks_diff(time.ticks_ms(), t1))

    def _send_telemetry(self) -> None:
        self.broker.set(key="telemetry", data=self.protocol.prepare_packet(self.telemetry.get_current_telemetry()))

    def _get_commands(self) -> list[tuple]:
        return self.protocol.parse_packet(packet=self.broker.get(key="cmd"))

    def _show_technical_info(self, cmd=None) -> None:
        if cmd is not None:
            self.viewer.show_tech_info(cmd)

    def _i_will_be_back(self) -> None:
        self.broker.close()
        self.networking.disconnect()


if __name__ == "__main__":
    robot = Robot()
    robot.run()
