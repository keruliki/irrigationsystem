import time
import requests
import math
import random
import pyowm
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

pumpPin = 23
valvePin = 24

GPIO.setup(pumpPin, GPIO.OUT) # GPIO Assign mode
GPIO.setup(valvePin, GPIO.OUT) # GPIO Assign mode

GPIO.output(valvePin, GPIO.LOW) # off
GPIO.output(pumpPin, GPIO.LOW) # off


owm = pyowm.OWM('da3d731cc410c8860168bb71afbdf932') #OpenWeather Token
TOKEN = "BBFF-AMtgI15oK55PzsfaGpYtRNJEKeuuNP"  # Put your TOKEN here
DEVICE_LABEL = "raspberrypi"  # Put your device label here 
VARIABLE_LABEL_1 = "humidity"  # Put your first variable label here
VARIABLE_LABEL_2 = "temperature"  # Put your second variable label here
VARIABLE_LABEL_3 = "turbidity"  # Put your second variable label here
VARIABLE_LABEL_4 = "waterlevel"  # Put your second variable label here

import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

#ADS1115 Gain
GAIN = 1



duration = 0
start = time.time()



observation = owm.weather_at_place('George Town, MY')
w = observation.get_weather()

value_1 = w.get_humidity()
value_2 = w.get_temperature('celsius')['temp']

def build_payload(variable_1, variable_2, variable_3, variable_4):
    # Creates two random values for sending data

    #Ready Turbidity
    turbidity = adc.read_adc(0, gain=GAIN)
    turbidity = turbidity/300
    turbidity = turbidity*100

    #Ready Water Level
    waterlevel = adc.read_adc(1, gain=GAIN)
    waterlevel = waterlevel/20000
    waterlevel = waterlevel*100
    
    print("Turbidity: " + str(turbidity) + "%")
    print("Water level: " + str(waterlevel) + "%")

    # Pause for half a second.
    time.sleep(0.5)

    global duration, value_1, value_2, start
    if duration <=300:
        
        print("Below 5 minutes")
        print(value_1)
        print(value_2)

        end = time.time()
    
    elif duration > 300:
        print("After 5 minutes seconds")
        observation = owm.weather_at_place('George Town, MY')
        w = observation.get_weather()

        value_1 = w.get_humidity()
        value_2 = w.get_temperature('celsius')['temp']


        start = time.time()
        end = time.time()

        if value_2 < 30:
            GPIO.output(pumpPin, GPIO.HIGH) # on
            print("PUMP ON")
            time.sleep(15)
            GPIO.output(pumpPin, GPIO.LOW) # off
            print("PUMP OFF")
        
        elif value_2 > 30:
            GPIO.output(pumpPin, GPIO.HIGH) # on
            print("PUMP ON")
            time.sleep(30)
            GPIO.output(pumpPin, GPIO.LOW) # off
            print("PUMP OFF")



    
    duration = end - start
    print(duration)

    if turbidity < 30:
        GPIO.output(valvePin, GPIO.HIGH) # on
        print("VALVE ON")
    
    else:
        GPIO.output(valvePin, GPIO.LOW) # off
        print("VALVE OFF")
    
    
    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: turbidity,
               variable_4: waterlevel}

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():

    
    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, VARIABLE_LABEL_4)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)