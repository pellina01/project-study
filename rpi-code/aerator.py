import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT, initial = 0)

def aerate(is_on):
    if is_on:
        GPIO.output(26,GPIO.HIGH)
    else:
        GPIO.output(26,GPIO.LOW)


