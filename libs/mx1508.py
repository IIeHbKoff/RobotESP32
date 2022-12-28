from machine import PWM
from config import Config


class MX1508:
    def __init__(self):
        self.pwm1_a = PWM(Config.motor1_a, freq=Config.motors_freq)
        self.pwm1_b = PWM(Config.motor1_b, freq=Config.motors_freq)
        self.pwm2_a = PWM(Config.motor2_a, freq=Config.motors_freq)
        self.pwm2_b = PWM(Config.motor2_b, freq=Config.motors_freq)

    def move_forward(self, speed: int) -> None:
        self.pwm1_a.duty_u16(self._get_speed(speed))
        self.pwm1_b.duty_u16(self._get_speed(0))
        self.pwm2_a.duty_u16(self._get_speed(speed))
        self.pwm2_b.duty_u16(self._get_speed(0))

    def move_backward(self, speed: int) -> None:
        self.pwm1_a.duty_u16(self._get_speed(0))
        self.pwm1_b.duty_u16(self._get_speed(speed))
        self.pwm2_a.duty_u16(self._get_speed(0))
        self.pwm2_b.duty_u16(self._get_speed(speed))

    def move_left(self, speed: int) -> None:
        self.pwm1_a.duty_u16(self._get_speed(speed))
        self.pwm1_b.duty_u16(self._get_speed(0))
        self.pwm2_a.duty_u16(self._get_speed(0))
        self.pwm2_b.duty_u16(self._get_speed(speed))

    def move_right(self, speed: int) -> None:
        self.pwm1_a.duty_u16(self._get_speed(0))
        self.pwm1_b.duty_u16(self._get_speed(speed))
        self.pwm2_a.duty_u16(self._get_speed(speed))
        self.pwm2_b.duty_u16(self._get_speed(0))

    def stop(self) -> None:
        self.pwm1_a.duty_u16(self._get_speed(0))
        self.pwm1_b.duty_u16(self._get_speed(0))
        self.pwm2_a.duty_u16(self._get_speed(0))
        self.pwm2_b.duty_u16(self._get_speed(0))

    def rotate_wheels(self, left_speed, right_speed):
        if left_speed > 0:
            self.pwm1_a.duty_u16(self._get_speed(left_speed))
            self.pwm1_b.duty_u16(self._get_speed(0))
        elif left_speed < 0:
            self.pwm1_a.duty_u16(self._get_speed(0))
            self.pwm1_b.duty_u16(self._get_speed(abs(left_speed)))
        else:
            self.pwm1_a.duty_u16(self._get_speed(0))
            self.pwm1_b.duty_u16(self._get_speed(0))

        if right_speed > 0:
            self.pwm2_a.duty_u16(self._get_speed(right_speed))
            self.pwm2_b.duty_u16(self._get_speed(0))
        elif right_speed < 0:
            self.pwm2_a.duty_u16(self._get_speed(0))
            self.pwm2_b.duty_u16(self._get_speed(abs(right_speed)))
        else:
            self.pwm2_a.duty_u16(self._get_speed(0))
            self.pwm2_b.duty_u16(self._get_speed(0))

    @staticmethod
    def _get_speed(speed) -> int:
        if speed == 0:
            return 0
        in_min = 1
        in_max = 100
        out_min = 30000
        out_max = 65000
        return int((speed - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
