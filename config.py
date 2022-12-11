from machine import Pin, SPI, I2C


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
    sck_pin = Pin(4, Pin.OUT)
    mosi_pin = Pin(2, Pin.OUT)
    ss_pin = Pin(0, Pin.OUT)
    # Other constants
    spi_baudrate = 10000000

    # I2C
    # Pins:
    scl = Pin(22, Pin.OUT)
    sda = Pin(21, Pin.OUT)
    # Other constants
    i2c_freq = 100000
    servos_channels = {
        "head": {"number": 0, "is_inverted": False},
        "right_arm": {"number": 1, "is_inverted": False},
        "left_arm": {"number": 2, "is_inverted": True}
    }
    servo_board_i2c_addr = 0x40

    wifi_ssid = 'Alex-iPhone'
    wifi_password = 'sb648qshx17zu'

    spi_1 = SPI(1, baudrate=spi_baudrate, sck=sck_pin, mosi=mosi_pin)
    i2c_0 = I2C(0, scl=scl, sda=sda, freq=i2c_freq)
