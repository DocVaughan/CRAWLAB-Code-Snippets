import Adafruit_BBIO.PWM as PWM

class Servo():

    def __init__(self, servo_pin):
        # Define duty cycle parameters for all servos
        self.duty_min = 3.
        self.duty_max = 14.5
        self.duty_span = self.duty_max - self.duty_min
        self.duty_mid = ((90.0 / 180) * self.duty_span + self.duty_min)
        
        self.servo_pin = servo_pin
        print 'starting servo PWM'
        PWM.start(self.servo_pin, self.duty_mid, 60.0)

    def set_servo_angle(self, angle):
        angle_f = float(angle)
        duty = ((angle_f / 180) * self.duty_span + self.duty_min)
        PWM.set_duty_cycle(self.servo_pin, duty)

    def close_servo(self):
        PWM.stop(self.servo_pin)
        PWM.cleanup()


if __name__ == "__main__":

    servo1 = Servo("P9_29")

    while True:
        angle = raw_input("Angle (0 to 180 x to exit):")
        if angle == 'x':
            servo1.close_servo()
            break

        servo1.set_servo_angle(angle)