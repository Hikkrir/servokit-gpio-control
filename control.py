import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

GPIO.setmode(GPIO.BCM)

class Control():
    """
    Класс для контроля сервоприводом и двигателем.
    BCM pinout.
    По умолчанию инициализирует пины rasberry pi 3:
        ШИМ -- 12
        IN1 двигателя -- 25
        IN2 двигателя -- 21
    """
    def __init__(self, pwm_pin = 12, IN1 = 25, IN2 = 21, 
                frequency = 20000, channels = 16):
        self.pwm_pin = pwm_pin
        self.IN1 = IN1
        self.IN2 = IN2
        self.channels = channels
        self.frequency = frequency
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, self.frequency)
        self.pwm.start(0)
        self.kit = ServoKit(channels = self.channels)

    def change_angle_servo(self, angle, servo_pin = 0):
        self.kit.servo[servo_pin].angle = angle
    
    def move_forward(self, dutycycle):
        self.pwm.ChangeDutyCycle(dutycycle)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
    
    def move_backward(self, dutycycle):
        self.pwm.ChangeDutyCycle(dutycycle)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)