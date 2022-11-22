from machine import PWM
from config import Config


class MovementSkill:
    def __init__(self):
        self.pwm1_a = PWM(Config.motor1_a, freq=Config.motors_freq)
        self.pwm1_b = PWM(Config.motor1_b, freq=Config.motors_freq)
        self.pwm2_a = PWM(Config.motor2_a, freq=Config.motors_freq)
        self.pwm2_b = PWM(Config.motor2_b, freq=Config.motors_freq)

    def move_forward(self, speed: int):
        self.pwm1_a.duty_u16(30000)
        self.pwm1_b.duty_u16(0)
        self.pwm2_a.duty_u16(30000)
        self.pwm2_b.duty_u16(0)

    def move_backward(self, speed: int):
        self.pwm1_a.duty_u16(0)
        self.pwm1_b.duty_u16(30000)
        self.pwm2_a.duty_u16(0)
        self.pwm2_b.duty_u16(30000)

    def move_left(self, speed: int):
        self.pwm1_a.duty_u16(30000)
        self.pwm1_b.duty_u16(0)
        self.pwm2_a.duty_u16(0)
        self.pwm2_b.duty_u16(30000)

    def move_right(self, speed: int):
        self.pwm1_a.duty_u16(0)
        self.pwm1_b.duty_u16(30000)
        self.pwm2_a.duty_u16(30000)
        self.pwm2_b.duty_u16(0)

    def stop(self):
        self.pwm1_a.duty_u16(0)
        self.pwm1_b.duty_u16(0)
        self.pwm2_a.duty_u16(0)
        self.pwm2_b.duty_u16(0)
