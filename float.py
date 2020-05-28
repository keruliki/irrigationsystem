import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


floatpin = 18


GPIO.setup(floatpin,GPIO.IN)

while(True):
    if GPIO.input(floatpin) == True:
        print("Water level high")

    else:
        print("Water level low")