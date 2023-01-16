class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self._i2c = i2c
        self._addr = addr
        # self._i2c.start()
        self._i2c.writeto(self._addr, bytearray([107, 0]))
        # self._i2c.stop()

    def _get_raw_values(self):
        # self._i2c.start()
        a = self._i2c.readfrom_mem(self._addr, 0x3B, 14)
        # self._i2c.stop()
        return a

    def _get_ints(self):
        b = self._get_raw_values()  # ?????????  is Iter?????
        c = list()
        for i in b:
            c.append(i)
        return c
    
    @staticmethod
    def _bytes_to_int(first_byte, second_byte):
        if not first_byte & 0x80:
            return first_byte << 8 | second_byte
        return - (((first_byte ^ 255) << 8) | (second_byte ^ 255) + 1)

    def get_values(self):
        raw_ints = self._get_raw_values()
        return {"AcX": self._bytes_to_int(raw_ints[0], raw_ints[1]),
                "AcY": self._bytes_to_int(raw_ints[2], raw_ints[3]),
                "AcZ": self._bytes_to_int(raw_ints[4], raw_ints[5]),
                "Tmp": self._bytes_to_int(raw_ints[6], raw_ints[7]) / 340.00 + 36.53,
                "GyX": self._bytes_to_int(raw_ints[8], raw_ints[9]),
                "GyY": self._bytes_to_int(raw_ints[10], raw_ints[11]),
                "GyZ": self._bytes_to_int(raw_ints[12], raw_ints[13])}
