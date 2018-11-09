# bme680-mqtt-micropython
Publish data from the bme680 sensor over MQTT using micropython. Makes use of:
* https://github.com/gkluoe/bme680/blob/master/library/bme680/i2c.py
* https://github.com/pimoroni/bme680
Am using in my leak sensor rig:
* https://www.hackster.io/robin-cole/micropython-leak-detector-with-adafruit-and-home-assistant-a2fa9e

[On Wipy 3](https://docs.pycom.io/datasheets/development/wipy3#pinout), P9 = SDA and P10 = SCL.
Read sensor bytes using `machine` with:
```python
from machine import I2C
i2c = I2C(0)   # using defauls P9 and P10
i2c.scan() # returns [119] which is hex 0x77
i2c.readfrom(0x77, 5) # read 5 bytes
```


<img src="https://github.com/robmarkcole/bme680-mqtt-micropython/blob/master/BME680-wipy.JPG">
