from networking.network_connection import NetworkConnection
from skills.protocol import Protocol


class Robot:
    def __init__(self):
        self.networking = NetworkConnection()
        self.protocol = Protocol()

    def live(self):
        self.networking.connect_to_wifi()
        self.networking.create_socket()

    def the_end(self):
        self.networking.disconnect()


if __name__ == "__main__":
    robot = Robot()
    robot.live()
    robot.the_end()
