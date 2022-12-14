from time import sleep

from networking.network_connection import NetworkConnection
import skills
from common_files.protocol import Protocol


class Robot:
    def __init__(self):
        self.networking = NetworkConnection()
        self.protocol = Protocol(skill_dict=skills.skill_dict)
        self.viewer = skills.FaceViewSkill()

    def live(self):
        self.viewer.show_tech_info("connecting")
        addr = self.networking.connect_to_wifi()
        self.viewer.show_tech_info(str(addr))
        self.networking.create_socket()
        self.viewer.show_tech_info("smile")
        sleep(1)
        self.viewer.show_tech_info("void")
        while True:
            answer_list = list()
            packet = self.networking.receive_from_socket()
            skill_list = self.protocol.parse_packet(packet=packet)
            for skill, params in skill_list:
                answer_list.append(skill().run(params))
            self.networking.send_to_socket(self.protocol.prepare_packet(data=answer_list))

    def the_end(self):
        self.networking.disconnect()


if __name__ == "__main__":
    robot = Robot()
    robot.live()
    robot.the_end()
