from machine import SPI, I2C
from time import sleep

from config import Config
from networking.network_connection import NetworkConnection
from networking.protocol import Protocol
from skills import FaceViewer, MovementSkill, Servos


class Robot:
    def __init__(self):
        spi_1 = SPI(1, baudrate=Config.spi_baudrate, sck=Config.sck_pin, mosi=Config.mosi_pin)
        i2c_0 = I2C(0, scl=Config.scl, sda=Config.sda, freq=Config.i2c_freq)
        self.wheels = MovementSkill()
        self.head = FaceViewer(spi_1)
        self.networking = NetworkConnection()
        self.protocol = Protocol()
        self.servo_board = Servos(i2c=i2c_0, inverted_channels=(2,))
        self.servo_head_channel = 0
        self.servo_right_arm_channel = 1
        self.servo_left_arm_channel = 2

    def live(self):
        self.networking.connect_to_wifi()
        self.networking.create_socket()
        self.head.show_mood("connected")
        sleep(1)
        self.head.display.fill(0)
        while True:
            list_packets = self.networking.receive_from_socket()
            for packet in list_packets:
                action, value = self.protocol.parse_packet(packet=packet)
                self.do_something(action, value)

    def do_something(self, action, value):
        if action == "right_hand":
            self.servo_board.position(index=self.servo_right_arm_channel, degrees=value)
        elif action == "left_hand":
            self.servo_board.position(index=self.servo_left_arm_channel, degrees=value)
        elif action == "head":
            self.servo_board.position(index=self.servo_head_channel, degrees=value)
        elif action == "left_wheel":
            self.wheels.move_left(speed=value)
        elif action == "right_wheel":
            self.wheels.move_right(speed=value)
        elif action == "mood":
            if value == "smile":
                self.head.show_mood("smile")
            elif value == "sad":
                self.head.show_mood("sad")
            elif value == "neutral":
                self.head.show_mood("neutral")
            elif value == "winking_left_eye":
                self.head.show_mood("smile")
                sleep(0.5)
                self.head.show_mood("winking_left_eye")
                sleep(0.5)
                self.head.show_mood("smile")
            elif value == "winking_right_eye":
                self.head.show_mood("smile")
                sleep(0.5)
                self.head.show_mood("winking_right_eye")
                sleep(0.5)
                self.head.show_mood("smile")


if __name__ == "__main__":
    robot = Robot()
    robot.live()
