import time

from config import Config
import socket
import network


class NetworkConnection:
    def __init__(self):
        self.wifi = None
        self.sock: socket.socket = None
        self.conn = None
        self.addr = None

    def connect_to_wifi(self):
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        self.wifi.disconnect()
        self.wifi.connect(Config.wifi_ssid, Config.wifi_password)
        while not self.wifi.isconnected():
            time.sleep(1)
        print(self.wifi.ifconfig())
        return True

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 8011))
        self.sock.listen(1)

    def receive_from_socket(self):
        if not self.conn or not self.addr:
            self.conn, self.addr = self.sock.accept()
        packets = list()
        while True:
            data = self.conn.recv(6)
            if not data:
                break
            packets.append(data)
        self.conn.close()
        self.conn = None
        return packets

    def disconnect(self):
        self.sock.close()
        self.sock = None
        self.conn = None
        self.addr = None
