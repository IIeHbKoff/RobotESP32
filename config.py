from machine import Pin, SPI, I2C


class Config:
    firmware_version = "1.0.0"
    # Moving settings
    # Pins:
    motor1_a = Pin(2)
    motor1_b = Pin(4)
    motor2_a = Pin(16)
    motor2_b = Pin(17)
    # Other constants
    motors_freq = 100

    # SPI
    # Pins:
    sck_pin = Pin(5, Pin.OUT)
    mosi_pin = Pin(18, Pin.OUT)
    ss_pin = Pin(19, Pin.OUT)
    # Other constants
    spi_baudrate = 10000000

    # I2C
    # Pins:
    scl = Pin(22, Pin.OUT)
    sda = Pin(21, Pin.OUT)
    # Other constants
    i2c_freq = 100000
    servo_board_i2c_addr = 0x40

    spi_1 = SPI(1, baudrate=spi_baudrate, sck=sck_pin, mosi=mosi_pin)
    i2c_0 = I2C(0, scl=scl, sda=sda, freq=i2c_freq)
