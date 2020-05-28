import pyowm
import time

owm = pyowm.OWM('da3d731cc410c8860168bb71afbdf932')  # You MUST provide a valid API key

# Have a pro subscription? Then use:
# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

# Search for current weather in London (Great Britain)
observation = owm.weather_at_place('George Town, MY')
w = observation.get_weather()
print(w)                      # <Weather - reference time=2013-12-18 09:20,
                              # status=Clouds>

# Weather details
print(w.get_wind())                 # {'speed': 4.6, 'deg': 330}
print(w.get_humidity())             # 87
print(w.get_temperature('celsius')['temp']) # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

time.sleep(2)