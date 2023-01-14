import time

from common_files import Constants
import socket
import network

from common_files.protocol import Protocol


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
        self.wifi.connect(Constants.WIFI_SSID, Constants.WIFI_PASSWORD)
        while not self.wifi.isconnected():
            time.sleep(1)
        return self.wifi.ifconfig()

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 8011))
        self.sock.listen(1)

    def receive_from_socket(self):
        if not self.conn or not self.addr:
            self.conn, self.addr = self.sock.accept()
        received_bytes = list()
        packet_started = False
        while True:
            symbol = self.conn.recv(1)
            if symbol == Protocol.start_symbol.encode():
                packet_started = True
                continue
            elif symbol == Protocol.end_symbol.encode():
                break
            if packet_started:
                received_bytes.append(symbol.decode())
        # self.conn.close()
        # self.conn = None
        return "".join(received_bytes)

    def send_to_socket(self, packet: str):
        if not self.conn or not self.addr:
            self.conn, self.addr = self.sock.accept()
        self.conn.send(packet.encode())

    def disconnect(self):
        self.sock.close()
        self.sock = None
        self.conn = None
        self.addr = None
