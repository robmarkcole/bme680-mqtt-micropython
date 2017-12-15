#!/usr/bin/env python
import bme680
from i2c import I2CAdapter
from mqtt import MQTTClient
import time
import machine


# timeout for mqtt
def settimeout(duration):
    pass


# Function for taking average of 100 analog readings
def smooth_reading():
    avg = 0
    _AVG_NUM = 100
    for _ in range(_AVG_NUM):
        avg += apin()
    avg /= _AVG_NUM
    return(avg)


# MQTT setup
client = MQTTClient("wipy", "192.168.0.30", port=1883)
client.settimeout = settimeout
client.connect()
mqtt_topic = "bme680"

# bme680
i2c_dev = I2CAdapter()
sensor = bme680.BME680(i2c_device=i2c_dev)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

# Moisture sensor
adc = machine.ADC()
apin = adc.channel(pin='P16', attn=3)

print("Polling:")
try:
    while True:
        if sensor.get_sensor_data():

            output = "{} C, {} hPa, {} RH, {} RES,".format(
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity,
                sensor.data.gas_resistance)

            print(output)
            client.publish(mqtt_topic, output)
            # Publish on individual topics for consistency with rpi repo.
            client.publish('bme680-humidity', str(sensor.data.humidity))
            client.publish('bme680-temperature', str(sensor.data.temperature))
            client.publish('bme680-pressure', str(sensor.data.pressure))
            client.publish('bme680-air_qual', str(sensor.data.gas_resistance))

            # Read the analogue water sensor
            _THRESHOLD = 3000
            analog_val = smooth_reading()
            print(analog_val)
            if analog_val < _THRESHOLD:
                print("Water_detected!")
                client.publish('bme680-water', "ON")
            else:
                client.publish('bme680-water', "OFF")
            time.sleep(2)

except KeyboardInterrupt:
    pass
