from machine import Pin


class Config:
    # Moving settings
    # Pins:
    motor1_a = Pin(18, Pin.OUT)
    motor1_b = Pin(19, Pin.OUT)
    motor2_a = Pin(17, Pin.OUT)
    motor2_b = Pin(5, Pin.OUT)
    # Other constants
    motors_freq = 100

    # SPI
    # Pins:
    sck_pin = Pin(4)
    mosi_pin = Pin(2)
    ss_pin = Pin(0)
    # Other constants
    spi_baudrate = 10000000
