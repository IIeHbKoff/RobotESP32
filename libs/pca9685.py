import ustruct
import time


class PCA9685:
    def __init__(self, i2c, inverted_channels=tuple(), address=0x40, freq=50, min_us=600, max_us=2400, degrees=180):
        self._i2c = i2c
        self._address = address
        self._freq = freq
        self._period = 1000000 / freq
        self._min_duty = self._us2duty(min_us)
        self._max_duty = self._us2duty(max_us)
        self._degrees = degrees
        self._inverted_channels = inverted_channels
        self._reset()

    def position(self, index, degrees=None, us=None, duty=None):
        span = self._max_duty - self._min_duty
        if degrees is not None:
            duty = self._min_duty + span * (
                degrees if index not in self._inverted_channels else 180 - degrees) / self._degrees
        elif us is not None:
            duty = self._us2duty(us)
        elif duty is not None:
            pass
        else:
            return self.duty(index)
        duty = min(self._max_duty, max(self._min_duty, int(duty)))
        self.duty(index, duty)

    def duty(self, index, value=None, invert=False):
        if value is None:
            pwm = self._pwm(index)
            if pwm == (0, 4096):
                value = 0
            elif pwm == (4096, 0):
                value = 4095
            value = pwm[1]
            if invert:
                value = 4095 - value
            return value
        if not 0 <= value <= 4095:
            raise ValueError("Out of range")
        if invert:
            value = 4095 - value
        if value == 0:
            self._pwm(index, 0, 4096)
        elif value == 4095:
            self._pwm(index, 4096, 0)
        else:
            self._pwm(index, 0, value)

    def release(self, index):
        self.duty(index, 0)

    def _us2duty(self, value):
        return int(4095 * value / self._period)

    def _write(self, address, value):
        self._i2c.writeto_mem(self._address, address, bytearray([value]))

    def _read(self, address):
        return self._i2c.readfrom_mem(self._address, address, 1)[0]

    def _reset(self):
        self._write(0x00, 0x00)  # Mode1

    def _freq(self, freq=None):
        if freq is None:
            return int(25000000.0 / 4096 / (self._read(0xfe) - 0.5))
        prescale = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode = self._read(0x00)  # Mode 1
        self._write(0x00, (old_mode & 0x7F) | 0x10)  # Mode 1, sleep
        self._write(0xfe, prescale)  # Prescale
        self._write(0x00, old_mode)  # Mode 1
        time.sleep_us(5)
        self._write(0x00, old_mode | 0xa1)  # Mode 1, autoincrement on

    def _pwm(self, index, on=None, off=None):
        if on is None or off is None:
            data = self._i2c.readfrom_mem(self._address, 0x06 + 4 * index, 4)
            return ustruct.unpack('<HH', data)
        data = ustruct.pack('<HH', on, off)
        self._i2c.writeto_mem(self._address, 0x06 + 4 * index, data)
