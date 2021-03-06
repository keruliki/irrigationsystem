import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

print('Reading ADS1x15 values, press Ctrl-C to quit...')

while True:
    # Read all the ADC channel values in a list.

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